from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, hashlib, os

app = Flask(__name__)
app.secret_key = 'bizboard-secret-key-change-in-production'
DB = 'bizboard.db'

# ── CHANGE THIS PASSWORD ──────────────────────────────────────────
ADMIN_EMAIL = 'admin@bizboard.com'
ADMIN_PASSWORD = 'admin@123'

# ── DATABASE ──────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                org      TEXT    NOT NULL,
                field    TEXT    NOT NULL,
                email    TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                name       TEXT    NOT NULL,
                quantity   INTEGER NOT NULL DEFAULT 0,
                price      REAL    NOT NULL DEFAULT 0,
                detail     TEXT,
                created_at TEXT    DEFAULT (date('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        db.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── ROUTES ────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        org      = request.form.get('org', '').strip()
        field    = request.form.get('field', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not all([org, field, email, password]):
            flash('All fields are required.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        else:
            try:
                with get_db() as db:
                    db.execute(
                        'INSERT INTO users (org, field, email, password) VALUES (?, ?, ?, ?)',
                        (org, field, email, hash_password(password))
                    )
                    db.commit()
                flash('Account created! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('An account with this email already exists.', 'error')

    return render_template('auth.html', page='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        with get_db() as db:
            user = db.execute(
                'SELECT * FROM users WHERE email = ? AND password = ?',
                (email, hash_password(password))
            ).fetchone()

        if user:
            session['user_id'] = user['id']
            session['org']     = user['org']
            session['field']   = user['field']
            session['email']   = user['email']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth.html', page='login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db() as db:
        products = db.execute(
            'SELECT * FROM products WHERE user_id = ? ORDER BY id DESC',
            (session['user_id'],)
        ).fetchall()

    total_qty   = sum(p['quantity'] for p in products)
    total_value = sum(p['quantity'] * p['price'] for p in products)

    return render_template('dashboard.html',
        products=products,
        total_qty=total_qty,
        total_value=total_value
    )


@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    name     = request.form.get('name', '').strip()
    quantity = request.form.get('quantity', '').strip()
    price    = request.form.get('price', '').strip()
    detail   = request.form.get('detail', '').strip()

    if not name or not quantity or not price:
        flash('Product name, quantity and price are required.', 'error')
        return redirect(url_for('dashboard'))

    try:
        qty = int(quantity)
        prc = float(price)
        if qty < 0 or prc < 0:
            raise ValueError
    except ValueError:
        flash('Enter valid numbers for quantity and price.', 'error')
        return redirect(url_for('dashboard'))

    with get_db() as db:
        db.execute(
            'INSERT INTO products (user_id, name, quantity, price, detail) VALUES (?, ?, ?, ?, ?)',
            (session['user_id'], name, qty, prc, detail)
        )
        db.commit()

    flash('Product added.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db() as db:
        db.execute(
            'DELETE FROM products WHERE id = ? AND user_id = ?',
            (product_id, session['user_id'])
        )
        db.commit()

    flash('Product removed.', 'success')
    return redirect(url_for('dashboard'))


# ── ADMIN ─────────────────────────────────────────────────────────

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    with get_db() as db:
        users = db.execute('SELECT * FROM users ORDER BY id').fetchall()
        products = db.execute(
            'SELECT p.*, u.org, u.email as user_email FROM products p JOIN users u ON p.user_id = u.id ORDER BY p.id DESC'
        ).fetchall()

    # Group products by user_id
    from collections import defaultdict
    user_products = defaultdict(list)
    for p in products:
        user_products[p['user_id']].append(p)

    # Compute per-user subtotals
    user_subtotals = {uid: sum(p['quantity'] * p['price'] for p in prods) for uid, prods in user_products.items()}

    total_users    = len(users)
    total_products = len(products)
    total_value    = sum(p['quantity'] * p['price'] for p in products)

    return render_template('admin.html',
        users=users,
        user_products=user_products,
        user_subtotals=user_subtotals,
        total_users=total_users,
        total_products=total_products,
        total_value=total_value
    )


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        print(email, password)
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            session['admin_email'] = email
            return redirect(url_for('admin'))
        else:
            error = 'Invalid admin credentials.'

    return render_template('admin_login.html', error=error)
    print(email, password)


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    session.pop('admin_email', None)
    return redirect(url_for('admin_login'))


# ── RUN ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

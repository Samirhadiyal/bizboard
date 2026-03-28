// ── DASHBOARD JS ─────────────────────────────────────────────────
// Handles the confirm dialog for product removal.
// (Form submission and flash messages are handled server-side by Flask.)

document.addEventListener('DOMContentLoaded', function () {

  // Confirm before removing a product
  document.querySelectorAll('.remove-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var name = form.dataset.name || 'this product';
      if (!confirm('Remove "' + name + '"?')) {
        e.preventDefault();
      }
    });
  });

  // Auto-hide flash alerts after 4 seconds
  document.querySelectorAll('.alert').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 4000);
  });

});

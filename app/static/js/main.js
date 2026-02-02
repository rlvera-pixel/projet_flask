/**
 * Comprendeshi - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {

    // Mobile navbar toggle
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.getElementById('navMenu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Auto-dismiss flash messages after 5 seconds
    var flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.transition = 'opacity 0.3s';
            flash.style.opacity = '0';
            setTimeout(function() { flash.remove(); }, 300);
        }, 5000);
    });

    // Confirm before delete actions
    var deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm(form.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

});

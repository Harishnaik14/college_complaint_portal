document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.addEventListener('click', function () {
            document.body.classList.toggle('dark-theme');
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-theme')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
    }

    const form = document.getElementById('complaintForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            const subject = document.getElementById('id_subject').value.trim();
            const description = document.getElementById('id_description').value.trim();
            const category = document.getElementById('id_category').value;
            let message = '';

            if (!subject) {
                message += 'Please enter a subject.\n';
            }
            if (!description) {
                message += 'Please enter a description.\n';
            }
            if (!category) {
                message += 'Please select a category.\n';
            }
            if (message) {
                event.preventDefault();
                alert(message);
            }
        });
    }
});

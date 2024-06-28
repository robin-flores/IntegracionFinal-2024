
function showSection(sectionId) {

var sections = document.querySelectorAll('.section');
sections.forEach(function (section) {
    section.classList.add('hidden');
});

var selectedSection = document.getElementById(sectionId);
if (selectedSection) {
    selectedSection.classList.remove('hidden');
}
}




function togglePassword(userId) {
        var passwordSpan = document.getElementById('password-' + userId);
        var icon = document.getElementById('toggle-icon-' + userId);

        if (passwordSpan.textContent === '********') {
            passwordSpan.textContent = passwordSpan.getAttribute('data-password');
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            passwordSpan.textContent = '********';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
}



document.addEventListener('DOMContentLoaded', function() {
    const togglePasswordButtons = document.querySelectorAll('.toggle-password-button');

    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);


            if (targetInput.type === 'password') {
                targetInput.type = 'text';
                this.querySelector('.bi').classList.remove('bi-eye');
                this.querySelector('.bi').classList.add('bi-eye-slash');
            } else {
                targetInput.type = 'password';
                this.querySelector('.bi').classList.remove('bi-eye-slash');
                this.querySelector('.bi').classList.add('bi-eye');
            }
        });
    });
});


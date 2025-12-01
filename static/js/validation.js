// Валидация форм на клиенте
document.addEventListener('DOMContentLoaded', function() {
    // Валидация формы регистрации
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            let valid = true;
            
            // Проверка логина
            const login = document.getElementById('login');
            if (login.value.length < 6) {
                showError(login, 'Логин должен содержать минимум 6 символов');
                valid = false;
            } else if (!/^[a-zA-Z0-9]+$/.test(login.value)) {
                showError(login, 'Логин должен содержать только латинские буквы и цифры');
                valid = false;
            } else {
                clearError(login);
            }
            
            // Проверка пароля
            const password = document.getElementById('password');
            if (password.value.length < 8) {
                showError(password, 'Пароль должен содержать минимум 8 символов');
                valid = false;
            } else {
                clearError(password);
            }
            
            // Проверка подтверждения пароля
            const confirmPassword = document.getElementById('confirm_password');
            if (confirmPassword.value !== password.value) {
                showError(confirmPassword, 'Пароли не совпадают');
                valid = false;
            } else {
                clearError(confirmPassword);
            }
            
            // Проверка телефона
            const phone = document.getElementById('phone');
            if (!/^8\(\d{3}\)\d{3}-\d{2}-\d{2}$/.test(phone.value)) {
                showError(phone, 'Формат телефона: 8(XXX)XXX-XX-XX');
                valid = false;
            } else {
                clearError(phone);
            }
            
            if (!valid) {
                e.preventDefault();
            }
        });
    }
    
    // Валидация формы заявки
    const applicationForm = document.getElementById('application-form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(e) {
            const dateInput = document.getElementById('desired_start_date');
            if (!/^\d{2}\.\d{2}\.\d{4}$/.test(dateInput.value)) {
                showError(dateInput, 'Формат даты: ДД.ММ.ГГГГ');
                e.preventDefault();
            } else {
                clearError(dateInput);
            }
        });
    }
    
    function showError(input, message) {
        const formGroup = input.closest('.form-group') || input.closest('.mb-3');
        let errorDiv = formGroup.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger small mt-1';
            formGroup.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        input.classList.add('is-invalid');
    }
    
    function clearError(input) {
        const formGroup = input.closest('.form-group') || input.closest('.mb-3');
        const errorDiv = formGroup.querySelector('.error-message');
        
        if (errorDiv) {
            errorDiv.remove();
        }
        
        input.classList.remove('is-invalid');
    }
    
    // Реальная проверка уникальности логина
    const loginInput = document.getElementById('login');
    if (loginInput) {
        let timeout = null;
        
        loginInput.addEventListener('input', function() {
            clearTimeout(timeout);
            
            timeout = setTimeout(function() {
                if (loginInput.value.length >= 6) {
                    checkLoginAvailability(loginInput.value);
                }
            }, 500);
        });
    }
});

function checkLoginAvailability(login) {
    fetch(`/check_login?login=${encodeURIComponent(login)}`)
        .then(response => response.json())
        .then(data => {
            const loginInput = document.getElementById('login');
            if (!data.available) {
                showError(loginInput, 'Этот логин уже занят');
            }
        });
}
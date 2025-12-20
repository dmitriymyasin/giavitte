// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Добавление анимации fade-in для всех карточек
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Валидация формы регистрации в реальном времени
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('7') || value.startsWith('8')) {
                value = value.substring(1);
            }
            
            if (value.length > 0) {
                value = '+7(' + value.substring(0, 3) + ')-' + 
                        value.substring(3, 6) + '-' + 
                        value.substring(6, 8) + '-' + 
                        value.substring(8, 10);
            }
            e.target.value = value;
        });
    }
    
    // Функция для проверки доступности логина
    window.checkLogin = function() {
        const loginField = document.getElementById('loginField');
        const resultDiv = document.getElementById('loginCheckResult');
        const login = loginField.value.trim();
        
        if (!login) {
            resultDiv.innerHTML = '<span class="text-warning">Введите логин</span>';
            return;
        }
        
        if (login.length < 6) {
            resultDiv.innerHTML = '<span class="text-warning">Логин должен быть не менее 6 символов</span>';
            return;
        }
        
        // Проверка на кириллицу и цифры
        if (!/^[а-яА-ЯёЁ0-9]+$/.test(login)) {
            resultDiv.innerHTML = '<span class="text-warning">Только кириллица и цифры</span>';
            return;
        }
        
        // Показываем индикатор загрузки
        resultDiv.innerHTML = '<span class="text-info">Проверка...</span>';
        
        fetch(`/check_login?login=${encodeURIComponent(login)}`)
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    resultDiv.innerHTML = '<span class="text-success">✓ Логин доступен</span>';
                    loginField.classList.remove('is-invalid');
                    loginField.classList.add('is-valid');
                } else {
                    resultDiv.innerHTML = '<span class="text-danger">✗ Логин занят</span>';
                    loginField.classList.remove('is-valid');
                    loginField.classList.add('is-invalid');
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<span class="text-danger">Ошибка проверки</span>';
            });
    };
    
    // Обработка удаления карточек
    document.querySelectorAll('.delete-card').forEach(button => {
        button.addEventListener('click', function() {
            const cardId = this.dataset.cardId;
            const cardTitle = this.closest('.card-body').querySelector('.card-title').textContent;
            
            if (confirm(`Вы уверены, что хотите удалить карточку "${cardTitle}"?`)) {
                // Показываем индикатор загрузки
                const originalText = this.textContent;
                this.textContent = 'Удаление...';
                this.disabled = true;
                
                fetch(`/delete_card/${cardId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Анимация удаления
                        const card = this.closest('.col-md-6');
                        card.style.transition = 'all 0.3s';
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.8)';
                        
                        setTimeout(() => {
                            location.reload();
                        }, 300);
                    } else {
                        alert(data.message || 'Ошибка при удалении');
                        this.textContent = originalText;
                        this.disabled = false;
                    }
                })
                .catch(error => {
                    alert('Ошибка сети');
                    this.textContent = originalText;
                    this.disabled = false;
                });
            }
        });
    });
    
    // Показать/скрыть поле причины в форме администратора
    const rejectRadio = document.getElementById('rejectRadio');
    if (rejectRadio) {
        const reasonField = document.getElementById('reasonField');
        const reasonInput = document.querySelector('textarea[name="reason"]');
        
        document.querySelectorAll('input[name="action"]').forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'reject') {
                    reasonField.style.display = 'block';
                    setTimeout(() => {
                        reasonField.classList.add('show');
                    }, 10);
                    reasonInput.required = true;
                } else {
                    reasonField.classList.remove('show');
                    setTimeout(() => {
                        reasonField.style.display = 'none';
                    }, 300);
                    reasonInput.required = false;
                }
            });
        });
        
        // Проверить начальное состояние
        if (rejectRadio.checked) {
            reasonField.style.display = 'block';
            reasonField.classList.add('show');
            reasonInput.required = true;
        }
    }
    
    // Автоматическое скрытие алертов через 5 секунд
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Добавление класса для мобильной навигации
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            document.querySelector('.navbar-collapse').classList.toggle('show');
        });
    }
});
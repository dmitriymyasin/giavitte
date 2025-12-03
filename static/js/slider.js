class Slider {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.slides = this.container.querySelectorAll('.slide');
        this.currentSlide = 0;
        this.totalSlides = this.slides.length;
        this.interval = null;
        this.slideInterval = 3000; // 3 секунды
        
        this.init();
    }
    
    init() {
        // Создаем элементы управления
        this.createControls();
        
        // Показываем первый слайд
        this.showSlide(0);
        
        // Запускаем автоматическую смену слайдов
        this.startAutoSlide();
        
        // Обработчики событий
        this.container.addEventListener('mouseenter', () => this.stopAutoSlide());
        this.container.addEventListener('mouseleave', () => this.startAutoSlide());
    }
    
    createControls() {
        // Создаем кнопки управления
        const controls = document.createElement('div');
        controls.className = 'slider-controls';
        
        const prevBtn = document.createElement('button');
        prevBtn.className = 'slider-btn prev';
        prevBtn.innerHTML = '&#10094;';
        prevBtn.addEventListener('click', () => this.prevSlide());
        
        const nextBtn = document.createElement('button');
        nextBtn.className = 'slider-btn next';
        nextBtn.innerHTML = '&#10095;';
        nextBtn.addEventListener('click', () => this.nextSlide());
        
        controls.appendChild(prevBtn);
        controls.appendChild(nextBtn);
        this.container.appendChild(controls);
        
        // Создаем индикаторы слайдов
        const indicators = document.createElement('div');
        indicators.className = 'slider-indicators';
        indicators.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        `;
        
        for (let i = 0; i < this.totalSlides; i++) {
            const indicator = document.createElement('button');
            indicator.className = 'slider-indicator';
            indicator.style.cssText = `
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: none;
                background: ${i === 0 ? 'white' : 'rgba(255, 255, 255, 0.5)'};
                cursor: pointer;
                transition: background 0.3s;
            `;
            indicator.addEventListener('click', () => this.showSlide(i));
            indicators.appendChild(indicator);
        }
        
        this.container.appendChild(indicators);
        this.indicators = indicators.querySelectorAll('.slider-indicator');
    }
    
    showSlide(index) {
        // Корректируем индекс
        if (index >= this.totalSlides) index = 0;
        if (index < 0) index = this.totalSlides - 1;
        
        // Скрываем все слайды
        this.slides.forEach(slide => {
            slide.style.display = 'none';
            slide.style.opacity = '0';
        });
        
        // Показываем выбранный слайд
        this.slides[index].style.display = 'block';
        setTimeout(() => {
            this.slides[index].style.opacity = '1';
            this.slides[index].style.transition = 'opacity 0.5s ease';
        }, 10);
        
        // Обновляем индикаторы
        this.indicators.forEach((indicator, i) => {
            indicator.style.background = i === index ? 'white' : 'rgba(255, 255, 255, 0.5)';
        });
        
        this.currentSlide = index;
    }
    
    nextSlide() {
        this.showSlide(this.currentSlide + 1);
    }
    
    prevSlide() {
        this.showSlide(this.currentSlide - 1);
    }
    
    startAutoSlide() {
        if (this.interval) clearInterval(this.interval);
        this.interval = setInterval(() => this.nextSlide(), this.slideInterval);
    }
    
    stopAutoSlide() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

// Инициализация слайдера при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.getElementById('slider-container');
    if (sliderContainer) {
        new Slider('slider-container');
    }
});
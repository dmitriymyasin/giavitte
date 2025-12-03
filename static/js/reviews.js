document.addEventListener('DOMContentLoaded', function() {
    // Динамическая загрузка статистики
    if (document.querySelector('.course-stats')) {
        document.querySelectorAll('.course-stats').forEach(element => {
            const courseId = element.dataset.courseId;
            loadCourseStats(courseId, element);
        });
    }
    
    // Подтверждение удаления
    document.querySelectorAll('.delete-review').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) {
                e.preventDefault();
            }
        });
    });
    
    // Анимация звезд рейтинга
    document.querySelectorAll('.rating-stars i').forEach(star => {
        star.addEventListener('mouseover', function() {
            const rating = this.dataset.rating;
            highlightStars(rating);
        });
        
        star.addEventListener('mouseout', function() {
            resetStars();
        });
    });
});

function loadCourseStats(courseId, element) {
    fetch(`/api/course/${courseId}/reviews/stats`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                element.innerHTML = `
                    <div class="text-center">
                        <h4>${data.average_rating}/5</h4>
                        <div class="text-warning mb-2">
                            ${'★'.repeat(Math.round(data.average_rating))}${'☆'.repeat(5 - Math.round(data.average_rating))}
                        </div>
                        <small class="text-muted">${data.total_reviews} отзывов</small>
                    </div>
                `;
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

function highlightStars(rating) {
    document.querySelectorAll('.rating-stars i').forEach(star => {
        if (star.dataset.rating <= rating) {
            star.classList.add('text-warning');
        } else {
            star.classList.remove('text-warning');
            star.classList.add('text-muted');
        }
    });
}

function resetStars() {
    document.querySelectorAll('.rating-stars i').forEach(star => {
        star.classList.remove('text-warning', 'text-muted');
        star.classList.add('text-warning');
    });
}
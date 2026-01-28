// frontend/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize floating elements
    initFloatingElements();
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
});

function initFloatingElements() {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const floatingContainer = document.createElement('div');
        floatingContainer.className = 'floating-elements';
        
        for (let i = 0; i < 15; i++) {
            const element = document.createElement('div');
            element.className = 'floating-element';
            element.style.width = Math.random() * 60 + 20 + 'px';
            element.style.height = element.style.width;
            element.style.left = Math.random() * 100 + '%';
            element.style.top = Math.random() * 100 + '%';
            element.style.animationDelay = Math.random() * 5 + 's';
            element.style.animationDuration = (Math.random() * 3 + 4) + 's';
            floatingContainer.appendChild(element);
        }
        
        heroSection.appendChild(floatingContainer);
    }
}

function initScrollAnimations() {
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.cultural-card, .feature-box, .dashboard-card');
        elements.forEach(element => {
            const position = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (position < screenPosition) {
                element.classList.add('fade-in-up');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check
}

function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// AJAX helper functions
function makeAjaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX request failed:', error);
        showNotification('An error occurred. Please try again.', 'error');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Career recommendation functions
function loadCareerRecommendations() {
    const loadingElement = document.getElementById('recommendations-loading');
    const resultsElement = document.getElementById('recommendations-results');
    
    if (loadingElement) loadingElement.style.display = 'block';
    if (resultsElement) resultsElement.style.display = 'none';
    
    makeAjaxRequest('/ai/get-recommendations/')
        .then(data => {
            if (loadingElement) loadingElement.style.display = 'none';
            if (resultsElement) {
                resultsElement.style.display = 'block';
                displayRecommendations(data.recommendations);
            }
        });
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    recommendations.forEach(rec => {
        const card = createRecommendationCard(rec);
        container.appendChild(card);
    });
}

function createRecommendationCard(recommendation) {
    const card = document.createElement('div');
    card.className = 'col-md-6 mb-4';
    card.innerHTML = `
        <div class="cultural-card h-100">
            <div class="card-body">
                <h5 class="card-title">${recommendation.job_title}</h5>
                <div class="progress cultural mb-3">
                    <div class="progress-bar" style="width: ${recommendation.compatibility_score}%">
                        ${recommendation.compatibility_score}% Match
                    </div>
                </div>
                <p><strong>Category:</strong> ${recommendation.category}</p>
                <p><strong>Experience Level:</strong> ${recommendation.experience_level}</p>
                <p><strong>Salary Range:</strong> ${recommendation.salary_range}</p>
                <button class="btn btn-odisha btn-sm" onclick="viewLearningPath('${recommendation.job_title}')">
                    View Learning Path
                </button>
            </div>
        </div>
    `;
    return card;
}

function viewLearningPath(jobTitle) {
    makeAjaxRequest(`/ai/get-learning-path/?job_title=${encodeURIComponent(jobTitle)}`)
        .then(data => {
            showLearningPathModal(jobTitle, data.path);
        });
}

function showLearningPathModal(jobTitle, learningPath) {
    // Implementation for showing learning path modal
    console.log('Learning path for:', jobTitle, learningPath);
}
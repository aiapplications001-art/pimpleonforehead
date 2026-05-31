// MyMirror Shared Interactive Logic
// Handles: Reveal Animations, FAQ Toggles, and Common Navigation

function initReveal() {
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReveal);
} else {
    initReveal();
}

// 2. FAQ Accordion Logic
window.toggleFAQ = function(index) {
    const items = document.querySelectorAll('.faq-item');
    const isActive = items[index].classList.contains('active-faq');
    items.forEach(item => item.classList.remove('active-faq'));
    if (!isActive) items[index].classList.add('active-faq');
};

// 3. Remedy Showcase Logic
window.activateRemedy = function(id, color) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    const btn = document.getElementById(`btn-${id}`);
    if (btn) btn.classList.add('active');
    
    const stage = document.getElementById('remedy-stage');
    if (stage) stage.style.backgroundColor = color;
    
    document.querySelectorAll('.stage-content').forEach(c => c.classList.remove('active'));
    const content = document.getElementById(`content-${id}`);
    if (content) content.classList.add('active');
};

// 4. Image Swappers
window.swapBotanical = function(imgSrc) { updateImage('botanical-img', imgSrc, 'scale(0.95) rotate(2deg)'); };
window.swapClinical = function(imgSrc) { updateImage('clinical-img', imgSrc, 'scale(0.95) rotate(-2deg)'); };
window.swapOTC = function(imgSrc) { updateImage('otc-img', imgSrc, 'scale(0.95) rotate(2deg)'); };

function updateImage(id, src, transform) {
    const img = document.getElementById(id);
    if (!img || img.src.includes(src)) return;
    img.style.opacity = '0';
    img.style.transform = transform;
    setTimeout(() => {
        img.src = '/acne/forehead-acne/' + src;
        img.style.opacity = '1';
        img.style.transform = 'scale(1) rotate(0deg)';
    }, 300);
}

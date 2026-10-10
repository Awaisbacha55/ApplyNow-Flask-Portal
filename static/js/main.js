document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isVisible = mobileMenu.style.display === 'flex';
            mobileMenu.style.display = isVisible ? 'none' : 'flex';
        });
    }

    // 2. Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href').substring(1);
            // Only scroll if the link is just a hash (e.g. #application-form), not if it contains a full URL route
            if (targetId && document.getElementById(targetId)) {
                e.preventDefault();
                document.getElementById(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu if open
                if (mobileMenu) mobileMenu.style.display = 'none';
            }
        });
    });

    // 3. Live Character Counter for Cover Letter
    const coverLetterTextarea = document.getElementById('cover_letter');
    const charCountSpan = document.getElementById('char-count');
    const MAX_CHARS = 2000;

    if (coverLetterTextarea && charCountSpan) {
        const updateCount = () => {
            const count = coverLetterTextarea.value.length;
            charCountSpan.textContent = count;
            
            const counterContainer = charCountSpan.parentElement;
            counterContainer.classList.remove('limit-near', 'limit-reached');
            
            if (count > MAX_CHARS) {
                counterContainer.classList.add('limit-reached');
            } else if (count > MAX_CHARS - 100) {
                counterContainer.classList.add('limit-near');
            }
        };

        // Initialize on load
        updateCount();
        
        // Update on input
        coverLetterTextarea.addEventListener('input', updateCount);
    }

    // 4. Form Submission Loading State
    const form = document.getElementById('job-application-form');
    const submitBtn = document.getElementById('submit-btn');

    if (form && submitBtn) {
        form.addEventListener('submit', (e) => {
            // Basic client-side validation check before showing loader
            if (form.checkValidity()) {
                submitBtn.classList.add('loading');
                submitBtn.setAttribute('disabled', 'true');
            }
        });
    }
});

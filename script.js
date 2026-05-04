/* ===================================================
   Navbar — scroll-driven background + mobile toggle
   Works across all pages (multi-page architecture)
   =================================================== */

const header    = document.getElementById('site-header');
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('nav-links');

/* 1. Transparent → dark background on scroll */
function onScroll() {
    if (window.scrollY > 20) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* 2. Hamburger toggle */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.classList.toggle('open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
    });
}

/* 3. Close drawer when a link is clicked (mobile) */
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks) navLinks.classList.remove('open');
        if (navToggle) {
            navToggle.classList.remove('open');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
});

/* 4. Mark active page link based on current filename */
(function markActivePage() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (
            href === page ||
            (page === '' && href === 'index.html') ||
            (page === 'index.html' && href === 'index.html')
        ) {
            link.classList.add('active');
        }
    });
})();

/* 5. Footer year */
const yearEl = document.getElementById('footer-year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

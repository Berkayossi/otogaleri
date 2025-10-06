document.addEventListener('DOMContentLoaded', function () {
    const mobileMenu = document.getElementById('mobile-menu');
    const nav = document.getElementById('primary-nav');

    if (mobileMenu && nav) {
        mobileMenu.addEventListener('click', function () {
            const isOpen = nav.classList.toggle('active');
            mobileMenu.setAttribute('aria-expanded', String(isOpen));
        });
    }

    // Smooth scroll for internal anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId.length > 1) {
                const el = document.querySelector(targetId);
                if (el) {
                    e.preventDefault();
                    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // Modal open/close delegation
    document.body.addEventListener('click', function (e) {
        const openBtn = e.target.closest('[data-modal-open]');
        const closeBtn = e.target.closest('[data-modal-close]');

        if (openBtn) {
            const id = openBtn.getAttribute('data-modal-open');
            const modal = document.getElementById(id);
            if (modal) {
                modal.classList.add('open');
                modal.setAttribute('aria-hidden', 'false');
            }
        }

        if (closeBtn) {
            const modal = closeBtn.closest('.modal');
            if (modal) {
                modal.classList.remove('open');
                modal.setAttribute('aria-hidden', 'true');
            }
        }
    });

    // Feather icons
    if (window.feather && typeof window.feather.replace === 'function') {
        window.feather.replace();
    }

    // Vanta Waves background
    if (window.VANTA && window.VANTA.WAVES) {
        window.VANTA.WAVES({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00,
            minWidth: 200.00,
            scale: 1.00,
            scaleMobile: 1.00,
            color: 0x0,
            shininess: 35.00,
            waveHeight: 15.00,
            waveSpeed: 0.25,
            zoom: 1.00
        });
    }
});

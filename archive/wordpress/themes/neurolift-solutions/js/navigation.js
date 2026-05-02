/**
 * Navigation functionality
 *
 * @package NeuroLift_Solutions
 */

(function() {
    'use strict';

    // Mobile menu toggle
    const menuToggle = document.createElement('button');
    menuToggle.className = 'menu-toggle';
    menuToggle.setAttribute('aria-controls', 'primary-menu');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.innerHTML = '<span class="menu-toggle-icon"></span>';

    const navigation = document.querySelector('.main-navigation');
    if (navigation) {
        navigation.insertBefore(menuToggle, navigation.firstChild);

        menuToggle.addEventListener('click', function() {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !expanded);
            navigation.classList.toggle('toggled');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (navigation && navigation.classList.contains('toggled')) {
            if (!navigation.contains(event.target)) {
                menuToggle.setAttribute('aria-expanded', 'false');
                navigation.classList.remove('toggled');
            }
        }
    });

})();

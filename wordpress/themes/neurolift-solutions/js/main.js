/**
 * Main JavaScript functionality
 *
 * @package NeuroLift_Solutions
 */

(function($) {
    'use strict';

    $(document).ready(function() {

        // Sticky header on scroll
        let lastScrollTop = 0;
        const header = $('.site-header');
        
        $(window).scroll(function() {
            const scrollTop = $(this).scrollTop();
            
            if (scrollTop > 100) {
                header.addClass('scrolled');
            } else {
                header.removeClass('scrolled');
            }
            
            lastScrollTop = scrollTop;
        });

        // Animate elements on scroll
        function animateOnScroll() {
            $('.card, .content-section').each(function() {
                const elementTop = $(this).offset().top;
                const windowBottom = $(window).scrollTop() + $(window).height();
                
                if (elementTop < windowBottom - 100) {
                    $(this).addClass('animated');
                }
            });
        }

        $(window).on('scroll', animateOnScroll);
        animateOnScroll(); // Run on page load

        // External links open in new tab
        $('a').filter(function() {
            return this.hostname && this.hostname !== location.hostname;
        }).attr('target', '_blank').attr('rel', 'noopener noreferrer');

        // Skip link focus fix
        $('.skip-link').click(function(e) {
            const target = $(this).attr('href');
            $(target).attr('tabindex', '-1').focus();
        });

    });

})(jQuery);

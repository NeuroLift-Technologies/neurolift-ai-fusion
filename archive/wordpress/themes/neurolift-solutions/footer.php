<?php
/**
 * Footer template
 *
 * @package NeuroLift_Solutions
 */
?>

    </div><!-- #content -->

    <footer id="colophon" class="site-footer">
        <div class="container">
            <?php if (is_active_sidebar('footer-1') || is_active_sidebar('footer-2') || is_active_sidebar('footer-3')) : ?>
                <div class="footer-widgets">
                    <?php if (is_active_sidebar('footer-1')) : ?>
                        <div class="footer-column">
                            <?php dynamic_sidebar('footer-1'); ?>
                        </div>
                    <?php endif; ?>

                    <?php if (is_active_sidebar('footer-2')) : ?>
                        <div class="footer-column">
                            <?php dynamic_sidebar('footer-2'); ?>
                        </div>
                    <?php endif; ?>

                    <?php if (is_active_sidebar('footer-3')) : ?>
                        <div class="footer-column">
                            <?php dynamic_sidebar('footer-3'); ?>
                        </div>
                    <?php endif; ?>
                </div>
            <?php endif; ?>

            <div class="site-info">
                <p>&copy; <?php echo date('Y'); ?> <a href="<?php echo esc_url(home_url('/')); ?>">NeuroLift Solutions</a></p>
                <p>
                    <?php
                    printf(
                        esc_html__('Created for NeuroLift Technologies | Contact: %s', 'neurolift-solutions'),
                        '<a href="mailto:neuro.edge24@gmail.com">neuro.edge24@gmail.com</a>'
                    );
                    ?>
                </p>
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'footer',
                    'menu_id'        => 'footer-menu',
                    'container'      => 'nav',
                    'container_class' => 'footer-navigation',
                    'depth'          => 1,
                ));
                ?>
            </div>
        </div>
    </footer>
</div><!-- #page -->

<?php wp_footer(); ?>
</body>
</html>

<?php
/**
 * Main template file
 *
 * @package NeuroLift_Solutions
 */

get_header();
?>

<main id="primary" class="site-main">
    <div class="container">
        <?php
        if (have_posts()) :
            // Start the Loop
            while (have_posts()) :
                the_post();
                get_template_part('template-parts/content', get_post_type());
            endwhile;

            // Previous/next page navigation
            neurolift_the_posts_navigation();

        else :
            get_template_part('template-parts/content', 'none');
        endif;
        ?>
    </div>
</main>

<?php
get_sidebar();
get_footer();

<?php
/**
 * Template for displaying single posts
 *
 * @package NeuroLift_Solutions
 */

get_header();
?>

<main id="primary" class="site-main">
    <div class="container">
        <?php
        while (have_posts()) :
            the_post();
            get_template_part('template-parts/content', get_post_type());

            // Post navigation
            the_post_navigation(array(
                'prev_text' => '<span class="nav-subtitle">' . esc_html__('Previous:', 'neurolift-solutions') . '</span> <span class="nav-title">%title</span>',
                'next_text' => '<span class="nav-subtitle">' . esc_html__('Next:', 'neurolift-solutions') . '</span> <span class="nav-title">%title</span>',
            ));

            // Comments
            if (comments_open() || get_comments_number()) :
                comments_template();
            endif;

        endwhile;
        ?>
    </div>
</main>

<?php
get_sidebar();
get_footer();

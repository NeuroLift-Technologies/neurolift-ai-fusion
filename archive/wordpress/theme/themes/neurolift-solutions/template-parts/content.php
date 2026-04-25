<?php
/**
 * Template part for displaying posts
 *
 * @package NeuroLift_Solutions
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php
        if (is_singular()) :
            the_title('<h1 class="entry-title">', '</h1>');
        else :
            the_title('<h2 class="entry-title"><a href="' . esc_url(get_permalink()) . '" rel="bookmark">', '</a></h2>');
        endif;

        if ('post' === get_post_type()) :
        ?>
            <div class="entry-meta">
                <?php
                neurolift_posted_on();
                neurolift_posted_by();
                ?>
            </div>
        <?php endif; ?>
    </header>

    <?php if (has_post_thumbnail() && is_singular()) : ?>
        <div class="post-thumbnail">
            <?php the_post_thumbnail('large'); ?>
        </div>
    <?php endif; ?>

    <div class="entry-content">
        <?php
        if (is_singular()) :
            the_content();
        else :
            the_excerpt();
        endif;

        wp_link_pages(array(
            'before' => '<div class="page-links">' . esc_html__('Pages:', 'neurolift-solutions'),
            'after'  => '</div>',
        ));
        ?>
    </div>

    <?php if (is_singular()) : ?>
        <footer class="entry-footer">
            <?php
            $categories_list = get_the_category_list(esc_html__(', ', 'neurolift-solutions'));
            if ($categories_list) {
                printf('<span class="cat-links">' . esc_html__('Posted in %1$s', 'neurolift-solutions') . '</span>', $categories_list);
            }

            $tags_list = get_the_tag_list('', esc_html_x(', ', 'list item separator', 'neurolift-solutions'));
            if ($tags_list) {
                printf('<span class="tags-links">' . esc_html__('Tagged %1$s', 'neurolift-solutions') . '</span>', $tags_list);
            }
            ?>
        </footer>
    <?php endif; ?>
</article>

<?php
/**
 * NeuroLift Solutions Theme Functions
 *
 * @package NeuroLift_Solutions
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// Theme version
define('NEUROLIFT_VERSION', '1.0.0');

/**
 * Theme Setup
 */
function neurolift_setup() {
    // Add default posts and comments RSS feed links to head
    add_theme_support('automatic-feed-links');

    // Let WordPress manage the document title
    add_theme_support('title-tag');

    // Enable support for Post Thumbnails on posts and pages
    add_theme_support('post-thumbnails');
    set_post_thumbnail_size(1200, 630, true);

    // Register navigation menus
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'neurolift-solutions'),
        'footer'  => __('Footer Menu', 'neurolift-solutions'),
    ));

    // Switch default core markup to output valid HTML5
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ));

    // Add theme support for selective refresh for widgets
    add_theme_support('customize-selective-refresh-widgets');

    // Add support for custom logo
    add_theme_support('custom-logo', array(
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ));

    // Add support for custom background
    add_theme_support('custom-background', array(
        'default-color' => 'ffffff',
    ));

    // Add support for wide and full alignment
    add_theme_support('align-wide');

    // Add support for responsive embeds
    add_theme_support('responsive-embeds');

    // Add support for editor styles
    add_theme_support('editor-styles');
}
add_action('after_setup_theme', 'neurolift_setup');

/**
 * Set the content width in pixels
 */
function neurolift_content_width() {
    $GLOBALS['content_width'] = apply_filters('neurolift_content_width', 1200);
}
add_action('after_setup_theme', 'neurolift_content_width', 0);

/**
 * Register widget areas
 */
function neurolift_widgets_init() {
    register_sidebar(array(
        'name'          => __('Sidebar', 'neurolift-solutions'),
        'id'            => 'sidebar-1',
        'description'   => __('Add widgets here to appear in your sidebar.', 'neurolift-solutions'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));

    register_sidebar(array(
        'name'          => __('Footer 1', 'neurolift-solutions'),
        'id'            => 'footer-1',
        'description'   => __('Add widgets here to appear in your footer.', 'neurolift-solutions'),
        'before_widget' => '<section id="%1$s" class="footer-widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));

    register_sidebar(array(
        'name'          => __('Footer 2', 'neurolift-solutions'),
        'id'            => 'footer-2',
        'description'   => __('Add widgets here to appear in your footer.', 'neurolift-solutions'),
        'before_widget' => '<section id="%1$s" class="footer-widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));

    register_sidebar(array(
        'name'          => __('Footer 3', 'neurolift-solutions'),
        'id'            => 'footer-3',
        'description'   => __('Add widgets here to appear in your footer.', 'neurolift-solutions'),
        'before_widget' => '<section id="%1$s" class="footer-widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}
add_action('widgets_init', 'neurolift_widgets_init');

/**
 * Enqueue scripts and styles
 */
function neurolift_scripts() {
    // Main stylesheet
    wp_enqueue_style('neurolift-style', get_stylesheet_uri(), array(), NEUROLIFT_VERSION);

    // Navigation script
    wp_enqueue_script('neurolift-navigation', get_template_directory_uri() . '/js/navigation.js', array(), NEUROLIFT_VERSION, true);

    // Main script
    wp_enqueue_script('neurolift-main', get_template_directory_uri() . '/js/main.js', array('jquery'), NEUROLIFT_VERSION, true);

    // Comments
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'neurolift_scripts');

/**
 * Custom template tags for this theme
 */

/**
 * Prints HTML with meta information for the current post-date/time
 */
function neurolift_posted_on() {
    $time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';

    $time_string = sprintf($time_string,
        esc_attr(get_the_date(DATE_W3C)),
        esc_html(get_the_date())
    );

    $posted_on = sprintf(
        esc_html_x('Posted on %s', 'post date', 'neurolift-solutions'),
        '<a href="' . esc_url(get_permalink()) . '" rel="bookmark">' . $time_string . '</a>'
    );

    echo '<span class="posted-on">' . $posted_on . '</span>';
}

/**
 * Prints HTML with meta information for the current author
 */
function neurolift_posted_by() {
    $byline = sprintf(
        esc_html_x('by %s', 'post author', 'neurolift-solutions'),
        '<span class="author vcard"><a class="url fn n" href="' . esc_url(get_author_posts_url(get_the_author_meta('ID'))) . '">' . esc_html(get_the_author()) . '</a></span>'
    );

    echo '<span class="byline"> ' . $byline . '</span>';
}

/**
 * Display navigation to next/previous set of posts
 */
function neurolift_the_posts_navigation() {
    the_posts_navigation(array(
        'prev_text'          => __('Older posts', 'neurolift-solutions'),
        'next_text'          => __('Newer posts', 'neurolift-solutions'),
        'screen_reader_text' => __('Posts navigation', 'neurolift-solutions'),
    ));
}

/**
 * Custom excerpt length
 */
function neurolift_excerpt_length($length) {
    return 30;
}
add_filter('excerpt_length', 'neurolift_excerpt_length');

/**
 * Custom excerpt more
 */
function neurolift_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'neurolift_excerpt_more');

/**
 * Add custom classes to body
 */
function neurolift_body_classes($classes) {
    // Adds a class of hfeed to non-singular pages
    if (!is_singular()) {
        $classes[] = 'hfeed';
    }

    // Adds a class of no-sidebar when there is no sidebar present
    if (!is_active_sidebar('sidebar-1')) {
        $classes[] = 'no-sidebar';
    }

    return $classes;
}
add_filter('body_class', 'neurolift_body_classes');

/**
 * Add pingback url to head
 */
function neurolift_pingback_header() {
    if (is_singular() && pings_open()) {
        printf('<link rel="pingback" href="%s">', esc_url(get_bloginfo('pingback_url')));
    }
}
add_action('wp_head', 'neurolift_pingback_header');

/**
 * Cloudflare cache integration
 */
function neurolift_cloudflare_purge_cache($post_id) {
    // Only purge for published posts
    if (get_post_status($post_id) !== 'publish') {
        return;
    }

    // Get the post URL
    $post_url = get_permalink($post_id);

    // Trigger cache purge via Cloudflare API
    // This requires the Cloudflare plugin or custom implementation
    do_action('neurolift_purge_cloudflare_cache', $post_url);
}
add_action('save_post', 'neurolift_cloudflare_purge_cache');

/**
 * Security enhancements
 */

// Remove WordPress version from head
remove_action('wp_head', 'wp_generator');

// Remove RSD link
remove_action('wp_head', 'rsd_link');

// Remove wlwmanifest.xml
remove_action('wp_head', 'wlwmanifest_link');

// Disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');

/**
 * Performance optimizations
 */

// Disable emoji script
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// Remove jQuery migrate
function neurolift_remove_jquery_migrate($scripts) {
    if (!is_admin() && isset($scripts->registered['jquery'])) {
        $script = $scripts->registered['jquery'];
        if ($script->deps) {
            $script->deps = array_diff($script->deps, array('jquery-migrate'));
        }
    }
}
add_action('wp_default_scripts', 'neurolift_remove_jquery_migrate');

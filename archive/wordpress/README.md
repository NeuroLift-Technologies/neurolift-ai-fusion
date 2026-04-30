# NeuroLift Solutions WordPress Site

Complete WordPress site structure for **neuroliftsolutions.com** containing everything created for NeuroLift Technologies.

---

## 📁 Directory Structure

```
wordpress/
├── themes/
│   └── neurolift-solutions/         # Custom WordPress theme
│       ├── style.css                # Main stylesheet
│       ├── functions.php            # Theme functions and features
│       ├── index.php                # Main template file
│       ├── header.php               # Header template
│       ├── footer.php               # Footer template
│       ├── sidebar.php              # Sidebar template
│       ├── front-page.php           # Homepage template
│       ├── page.php                 # Page template
│       ├── single.php               # Single post template
│       ├── template-parts/          # Reusable template parts
│       │   ├── content.php          # Post content template
│       │   └── content-none.php     # No content template
│       └── js/                      # JavaScript files
│           ├── navigation.js        # Navigation functionality
│           └── main.js              # Main scripts
├── CONTENT-STRUCTURE.md             # Content organization guide
├── DEPLOYMENT-GUIDE.md              # Deployment instructions
└── README.md                        # This file
```

---

## 🎨 Theme Features

### Core Philosophy
Built on the principle **"Nothing About Us Without Us"** - by neurodivergent voices, for neurodivergent minds.

**Tagline:** "Human and AI Solidarity Without Singularity"

### Built-in Features
- **Responsive Design**: Mobile-first, fully responsive layout
- **Founder-Focused**: Dedicated template highlighting Joshua Dorsey's vision
- **Custom Logo Support**: Upload your own logo in the customizer
- **Navigation Menus**: Primary and footer menu locations
- **Widget Areas**: Sidebar and 3 footer widget areas
- **Featured Images**: Full support for post thumbnails
- **Custom Background**: Customize background colors
- **Cloudflare Integration**: Cache purging and optimization hooks
- **Security Hardened**: WordPress version hiding, XML-RPC disabled
- **Performance Optimized**: Emoji scripts removed, jQuery migrate disabled
- **Privacy-First Design**: Respects user sovereignty, no data mining

### Custom Styling
- **CSS Variables**: Easy theme color customization
- **Smooth Animations**: Scroll animations and transitions
- **Card Layouts**: Flexible grid system for content cards
- **Button Styles**: Primary and secondary button designs
- **Typography**: Clean, readable font system

---

## 🚀 Installation

### 1. Upload Theme

**Via WordPress Admin:**
1. Go to Appearance → Themes → Add New
2. Click "Upload Theme"
3. Choose the `neurolift-solutions.zip` file
4. Click "Install Now"
5. Activate the theme

**Via FTP:**
1. Upload the `neurolift-solutions` folder to `/wp-content/themes/`
2. Go to Appearance → Themes in WordPress admin
3. Activate "NeuroLift Solutions" theme

### 2. Configure Theme

1. **Set Homepage:**
   - Go to Settings → Reading
   - Select "A static page"
   - Choose your homepage as "Front page"

2. **Configure Menus:**
   - Go to Appearance → Menus
   - Create a new menu
   - Assign to "Primary Menu" location

3. **Add Widgets:**
   - Go to Appearance → Widgets
   - Add widgets to Sidebar and Footer areas

4. **Customize Theme:**
   - Go to Appearance → Customize
   - Configure Site Identity, Colors, Menus, Widgets

---

## 📄 Required Pages

Create these pages in WordPress for complete site functionality:

### Essential Pages
1. **Home** (Front Page) - Uses `front-page.php` template with founder's vision
2. **About the Founder** - Joshua Dorsey's story and philosophy (uses `page-founder.php`)
3. **About Us** - Company information and mission
4. **Technology** - Technical details and architecture
5. **Avatar System** - Explanation of Avatar-Aide-Advocate
6. **TOI-OTOI Framework** - "Human and AI Solidarity Without Singularity"
7. **Business Agents** - Agent-based business operations
8. **Cloudflare Integration** - Infrastructure and deployment
9. **Documentation** - Technical documentation and guides
10. **Blog** - News and updates
11. **Contact** - Contact information and form

### Additional Content Pages
- **Quickstart Guide** - Getting started with the system
- **Implementation Status** - Current development phase
- **Privacy Policy** - Data handling and privacy
- **Terms of Service** - Usage terms

---

## 🎯 Content Areas

### Homepage Sections (front-page.php)

The homepage includes these key sections:

1. **Hero Section**
   - Site name and tagline
   - Call-to-action buttons

2. **About Section**
   - Company overview
   - Three main features (AI Learning, TOI-OTOI, Agent Business)

3. **Innovation Features**
   - 6 key innovations with icons
   - Avatar System, Aide Coaching, Advocate Fusion
   - Privacy First, Cloudflare, Simulation

4. **Mission Statement**
   - "Nothing About Us Without Us" motto
   - Mission description

5. **Technology Stack**
   - Infrastructure details
   - AI & Simulation components
   - Security & Performance features

6. **Contact Section**
   - Email contact
   - Call-to-action buttons

---

## 🎨 Customization

### Color Scheme

Edit CSS variables in `style.css`:

```css
:root {
    --primary-color: #4A90E2;      /* Main brand color */
    --secondary-color: #50E3C2;    /* Accent color */
    --accent-color: #F5A623;       /* Highlight color */
    --dark-color: #2C3E50;         /* Dark text */
    --light-color: #ECF0F1;        /* Light background */
}
```

### Typography

Change fonts in `style.css`:

```css
:root {
    --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...;
    --font-secondary: Georgia, 'Times New Roman', serif;
}
```

### Layout

Adjust container widths:

```css
.container { max-width: 1200px; }
.container-wide { max-width: 1400px; }
.container-narrow { max-width: 800px; }
```

---

## 🔌 Integrations

### Cloudflare Integration

The theme includes Cloudflare cache purging:

```php
// Automatically purges cache when posts are updated
add_action('save_post', 'neurolift_cloudflare_purge_cache');
```

To use:
1. Install Cloudflare WordPress plugin
2. Configure API credentials
3. Cache will auto-purge on content updates

### Contact Forms

Recommended plugins:
- **Contact Form 7**: Simple and flexible
- **WPForms**: User-friendly with drag-and-drop
- **Gravity Forms**: Advanced features (premium)

### SEO

Recommended plugins:
- **Yoast SEO**: Comprehensive SEO toolkit
- **Rank Math**: Feature-rich alternative
- **All in One SEO**: Easy to use

---

## 🛠️ Development

### Local Development

1. **Install Local WordPress:**
   - Use Local by Flywheel, XAMPP, or MAMP
   - Set up WordPress installation

2. **Install Theme:**
   - Copy theme folder to `wp-content/themes/`
   - Activate in WordPress admin

3. **Enable Debugging:**
   ```php
   // wp-config.php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   define('WP_DEBUG_DISPLAY', false);
   ```

### Child Theme

To create a child theme:

1. Create folder: `neurolift-solutions-child`
2. Create `style.css`:
   ```css
   /*
   Theme Name: NeuroLift Solutions Child
   Template: neurolift-solutions
   */
   ```
3. Create `functions.php`:
   ```php
   <?php
   add_action('wp_enqueue_scripts', 'child_enqueue_styles');
   function child_enqueue_styles() {
       wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
   }
   ```

---

## 🔒 Security

### Implemented Security Features

1. **WordPress Version Hiding**: Removed from HTML head
2. **XML-RPC Disabled**: Prevents brute force attacks
3. **RSD Link Removed**: Reduces information disclosure
4. **Security Headers**: Added via Cloudflare Workers

### Additional Recommendations

1. **Install Security Plugin:**
   - Wordfence Security
   - Sucuri Security
   - iThemes Security

2. **Enable SSL:**
   - Use Cloudflare SSL (Full or Full Strict)
   - Force HTTPS in WordPress

3. **Regular Updates:**
   - Keep WordPress core updated
   - Update plugins regularly
   - Update theme when new versions available

4. **Strong Passwords:**
   - Use strong admin passwords
   - Enable 2FA (Two-Factor Authentication)

---

## ⚡ Performance

### Built-in Optimizations

1. **Emoji Scripts Removed**: Reduces HTTP requests
2. **jQuery Migrate Removed**: Smaller JavaScript footprint
3. **Cloudflare Caching**: Edge caching for static assets
4. **Responsive Images**: WordPress native support
5. **Lazy Loading**: Browser-native lazy loading

### Recommended Plugins

1. **WP Rocket**: Premium caching plugin
2. **Autoptimize**: Free JS/CSS optimization
3. **Imagify**: Image compression and optimization
4. **Query Monitor**: Debug and optimize queries

---

## 📱 Mobile Optimization

The theme is fully responsive with:
- Mobile-first design approach
- Touch-friendly navigation
- Optimized images for mobile
- Fast loading on mobile networks
- Readable typography on small screens

---

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## 📊 Analytics

### Google Analytics

Add tracking code in theme customizer or via plugin:
- **MonsterInsights**: Google Analytics for WordPress
- **GA Google Analytics**: Simple integration

### Cloudflare Analytics

Available in Cloudflare dashboard:
- Page views
- Unique visitors
- Bandwidth usage
- Threat analytics

---

## 🐛 Troubleshooting

### Common Issues

**Theme not displaying correctly:**
1. Clear browser cache
2. Purge Cloudflare cache
3. Check CSS/JS files are loading
4. Verify file permissions

**Menu not working:**
1. Go to Appearance → Menus
2. Create menu and assign location
3. Check navigation.js is loading

**Images not showing:**
1. Check file permissions (644 for files, 755 for folders)
2. Regenerate thumbnails with plugin
3. Verify image paths

**Performance issues:**
1. Install caching plugin
2. Optimize images
3. Check for plugin conflicts
4. Enable Cloudflare optimizations

---

## 📞 Support

### Resources

- **Theme Documentation**: This README and CONTENT-STRUCTURE.md
- **WordPress Codex**: https://codex.wordpress.org
- **WordPress Support**: https://wordpress.org/support/
- **Cloudflare Docs**: See `/docs/cloudflare/CLOUDFLARE_SETUP.md`

### Contact

- **Email**: neuro.edge24@gmail.com
- **Website**: neuroliftsolutions.com
- **Repository**: See main repository documentation

---

## 📝 License

This theme is licensed under GNU General Public License v2 or later.

---

## 🎉 Credits

**Developed by**: Joshua Dorsey  
**For**: NeuroLift Technologies  
**Website**: neuroliftsolutions.com  
**Version**: 1.0.0  
**Last Updated**: 2024

---

## 🚀 Next Steps

After installation:

1. ✅ Install and activate the theme
2. ✅ Configure homepage and menus
3. ✅ Create essential pages (see CONTENT-STRUCTURE.md)
4. ✅ Add widgets to sidebar and footer
5. ✅ Install recommended plugins
6. ✅ Configure Cloudflare integration
7. ✅ Set up contact forms
8. ✅ Enable SSL/HTTPS
9. ✅ Test on mobile devices
10. ✅ Launch and monitor!

For detailed content organization, see **CONTENT-STRUCTURE.md**  
For deployment instructions, see **DEPLOYMENT-GUIDE.md**

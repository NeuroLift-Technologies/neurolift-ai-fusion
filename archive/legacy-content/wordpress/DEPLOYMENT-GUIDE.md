# NeuroLift Solutions - WordPress Deployment Guide

Complete step-by-step guide for deploying the WordPress site to neuroliftsolutions.com

---

## 📋 Prerequisites

### Required Accounts & Access
- ✅ Domain registered: neuroliftsolutions.com (Northwest Registered Agent)
- ✅ Cloudflare account (neuro.edge24@gmail.com)
- ✅ WordPress hosting provider
- ✅ FTP/SFTP access credentials
- ✅ MySQL/MariaDB database access

### Required Tools
- FTP client (FileZilla, Cyberduck, or similar)
- Text editor (VS Code, Sublime Text, etc.)
- Web browser
- Terminal/Command line access

---

## 🚀 Deployment Steps

### Step 1: Set Up Cloudflare (If Not Already Done)

#### 1.1 Add Domain to Cloudflare
```bash
1. Log in to Cloudflare Dashboard (https://dash.cloudflare.com)
2. Click "Add a Site"
3. Enter: neuroliftsolutions.com
4. Select Free plan
5. Review and confirm DNS records
```

#### 1.2 Update Nameservers
```
At Northwest Registered Agent:
1. Log in to domain management
2. Find DNS/Nameserver settings
3. Replace with Cloudflare nameservers (provided after adding site)
4. Save changes
5. Wait for propagation (24-48 hours, usually faster)
```

#### 1.3 Configure Cloudflare Settings

**SSL/TLS:**
```
Dashboard → SSL/TLS → Overview
- Encryption mode: Full or Full (Strict)
- Enable: Always Use HTTPS
- Enable: Automatic HTTPS Rewrites
```

**Caching:**
```
Dashboard → Caching → Configuration
- Caching Level: Standard
- Browser Cache TTL: 4 hours
```

**Security:**
```
Dashboard → Security → Settings
- Security Level: Medium
- Enable: Bot Fight Mode
```

---

### Step 2: Set Up WordPress Hosting

#### 2.1 Choose Hosting Provider

**Recommended Providers:**
- **Cloudflare** (if available for WordPress)
- **SiteGround**: Excellent performance
- **WP Engine**: Premium managed WordPress
- **Kinsta**: High-performance hosting
- **Bluehost**: Budget-friendly option

#### 2.2 Install WordPress

**Option A: One-Click Install (Recommended)**
```
1. Log in to hosting control panel (cPanel/Plesk)
2. Find "WordPress Installer" or "Softaculous"
3. Click "Install"
4. Configure:
   - Domain: neuroliftsolutions.com
   - Directory: Leave blank (install in root)
   - Site Name: NeuroLift Solutions
   - Admin Username: [Choose secure username]
   - Admin Password: [Use strong password]
   - Admin Email: neuro.edge24@gmail.com
5. Click "Install"
```

**Option B: Manual Install**
```bash
# Download WordPress
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

# Upload files via FTP to public_html/ or www/
# Create database in hosting panel
# Visit domain and follow installation wizard
```

---

### Step 3: Upload NeuroLift Solutions Theme

#### 3.1 Prepare Theme Files

**Create Theme ZIP:**
```bash
cd /path/to/neurolift-ai-fusion/wordpress/themes
zip -r neurolift-solutions.zip neurolift-solutions/
```

#### 3.2 Upload via WordPress Admin (Recommended)

```
1. Log in to WordPress Admin (neuroliftsolutions.com/wp-admin)
2. Go to Appearance → Themes
3. Click "Add New"
4. Click "Upload Theme"
5. Choose neurolift-solutions.zip
6. Click "Install Now"
7. Click "Activate"
```

#### 3.3 Upload via FTP (Alternative)

```
1. Connect to server via FTP
2. Navigate to: /wp-content/themes/
3. Upload neurolift-solutions folder
4. Go to WordPress Admin → Appearance → Themes
5. Activate "NeuroLift Solutions"
```

---

### Step 4: Configure WordPress

#### 4.1 Basic Settings

**General Settings:**
```
Settings → General
- Site Title: NeuroLift Solutions
- Tagline: AI-Powered Neurodivergent Support & Intelligent Business Operations
- WordPress Address: https://neuroliftsolutions.com
- Site Address: https://neuroliftsolutions.com
- Email: neuro.edge24@gmail.com
- Timezone: [Your timezone]
```

**Permalinks:**
```
Settings → Permalinks
- Select: Post name
- Custom Structure: /%postname%/
- Save Changes
```

**Reading Settings:**
```
Settings → Reading
- Your homepage displays: A static page
- Homepage: [Select "Home" page]
- Posts page: [Select "Blog" page]
```

#### 4.2 Create Essential Pages

**Create these pages:**
```
Pages → Add New

1. Home
   - Title: Home
   - Content: [Leave blank, uses front-page.php template]
   - Publish

2. About
   - Title: About Us
   - Content: [Copy from CONTENT-STRUCTURE.md]
   - Publish

3. Avatar-Aide-Advocate
   - Title: Avatar-Aide-Advocate System
   - Content: [Copy from CONTENT-STRUCTURE.md]
   - Publish

4. TOI-OTOI Framework
5. Agent-Based Business
6. Technology
7. Cloudflare Integration
8. Documentation
9. Blog (for posts page)
10. Contact
```

#### 4.3 Set Up Menus

**Primary Menu:**
```
Appearance → Menus
1. Create new menu: "Primary Menu"
2. Add pages:
   - Home
   - About Us
     - Avatar-Aide-Advocate (sub-item)
     - TOI-OTOI Framework (sub-item)
     - Agent-Based Business (sub-item)
   - Technology
     - Architecture (sub-item)
     - Cloudflare Integration (sub-item)
   - Documentation
   - Blog
   - Contact
3. Assign to location: Primary Menu
4. Save Menu
```

**Footer Menu:**
```
1. Create new menu: "Footer Menu"
2. Add custom links:
   - Privacy Policy
   - Terms of Service
   - Quickstart
   - Status
3. Assign to location: Footer Menu
4. Save Menu
```

---

### Step 5: Install Essential Plugins

#### 5.1 Required Plugins

**Via WordPress Admin:**
```
Plugins → Add New

1. Cloudflare
   - Search: "Cloudflare"
   - Install and Activate official plugin
   - Configure with API token

2. Contact Form 7
   - Search: "Contact Form 7"
   - Install and Activate
   - Create contact form

3. Yoast SEO
   - Search: "Yoast SEO"
   - Install and Activate
   - Run configuration wizard

4. Wordfence Security
   - Search: "Wordfence Security"
   - Install and Activate
   - Complete setup wizard
```

#### 5.2 Recommended Plugins

```
5. WP Rocket (Premium) or Autoptimize (Free)
   - Caching and performance

6. Imagify or Smush
   - Image optimization

7. UpdraftPlus
   - Backup solution

8. Redirection
   - Manage 301 redirects
```

---

### Step 6: Configure Cloudflare Integration

#### 6.1 Connect Cloudflare Plugin

```
1. Get Cloudflare API Token:
   - Cloudflare Dashboard → My Profile → API Tokens
   - Create Token → "Edit Cloudflare Workers"
   - Copy token

2. WordPress Admin:
   - Settings → Cloudflare
   - Enter API Token
   - Select Zone: neuroliftsolutions.com
   - Save

3. Configure Settings:
   - Automatic Cache Purge: ON
   - Development Mode: OFF
   - Apply Default Settings
```

#### 6.2 Deploy Cloudflare Workers

```bash
# From repository root
cd cloudflare/workers

# Login to Wrangler (first time)
wrangler login

# Deploy WordPress optimizer
wrangler publish wordpress-optimizer.js --name neurolift-wordpress-optimizer

# Configure route in Cloudflare Dashboard
# Dashboard → Workers → Routes
# Add route: neuroliftsolutions.com/*
# Worker: neurolift-wordpress-optimizer
```

#### 6.3 Create Page Rules

```
Cloudflare Dashboard → Rules → Page Rules

Rule 1: Bypass Cache for Admin
- URL: neuroliftsolutions.com/wp-admin*
- Settings:
  • Cache Level: Bypass
  • Security Level: High

Rule 2: Cache Static Assets
- URL: neuroliftsolutions.com/wp-content/*
- Settings:
  • Cache Level: Cache Everything
  • Edge Cache TTL: 1 day

Rule 3: Cache Homepage
- URL: neuroliftsolutions.com/
- Settings:
  • Cache Level: Cache Everything
  • Edge Cache TTL: 1 hour
```

---

### Step 7: Security Hardening

#### 7.1 Update wp-config.php

```php
// Add these security constants
define('DISALLOW_FILE_EDIT', true);  // Disable theme/plugin editor
define('WP_AUTO_UPDATE_CORE', true); // Enable auto-updates
define('FORCE_SSL_ADMIN', true);     // Force SSL for admin

// Security keys (generate at https://api.wordpress.org/secret-key/1.1/salt/)
[Replace all security keys]
```

#### 7.2 Secure File Permissions

```bash
# Connect via SSH and run:
cd /path/to/wordpress

# Set directory permissions
find . -type d -exec chmod 755 {} \;

# Set file permissions
find . -type f -exec chmod 644 {} \;

# Protect wp-config.php
chmod 600 wp-config.php
```

#### 7.3 Add .htaccess Security Rules

```apache
# Add to .htaccess (if using Apache)

# Protect wp-config.php
<files wp-config.php>
    order allow,deny
    deny from all
</files>

# Disable directory browsing
Options -Indexes

# Protect .htaccess
<files .htaccess>
    order allow,deny
    deny from all
</files>
```

---

### Step 8: Performance Optimization

#### 8.1 Configure Caching Plugin

**WP Rocket (if installed):**
```
Settings → WP Rocket
- Cache:
  • Enable caching for mobile devices
  • Enable caching for logged-in users
- File Optimization:
  • Minify CSS files
  • Minify JavaScript files
  • Combine CSS files
- Media:
  • Enable LazyLoad for images
  • Enable LazyLoad for iframes
- Advanced:
  • Enable Google Fonts optimization
```

#### 8.2 Optimize Images

```
Media → Bulk Optimization
- Run bulk optimization on all images
- Set auto-optimization for future uploads
```

#### 8.3 Enable Cloudflare Optimizations

```
Cloudflare Dashboard → Speed → Optimization
- Auto Minify:
  ✓ JavaScript
  ✓ CSS
  ✓ HTML
- Brotli: ON
- Rocket Loader: OFF (conflicts with WordPress)
- Mirage: ON
- Polish: Lossy
```

---

### Step 9: Content Migration

#### 9.1 Create Content Pages

Use content from CONTENT-STRUCTURE.md:

```
For each page:
1. Pages → Add New
2. Enter title
3. Copy content from CONTENT-STRUCTURE.md
4. Format with headings, lists, emphasis
5. Add featured image
6. Optimize with Yoast SEO
7. Publish
```

#### 9.2 Create Initial Blog Posts

```
Posts → Add New

Suggested first posts:
1. "Introducing NeuroLift Technologies"
2. "The Avatar-Aide-Advocate Process Explained"
3. "Why Privacy-First AI Matters"
4. "Phase 1 Implementation Complete"
```

---

### Step 10: Testing & Quality Assurance

#### 10.1 Functionality Testing

**Test checklist:**
```
✓ Homepage loads correctly
✓ All menu links work
✓ Internal page navigation
✓ Contact form submits
✓ Mobile responsive display
✓ SSL certificate active
✓ Blog posts display
✓ Search functionality
✓ Comments (if enabled)
✓ Widget areas display
```

#### 10.2 Performance Testing

**Tools to use:**
```
1. Google PageSpeed Insights
   https://pagespeed.web.dev/
   - Target: 90+ for mobile and desktop

2. GTmetrix
   https://gtmetrix.com/
   - Target: Grade A, < 3s load time

3. WebPageTest
   https://www.webpagetest.org/
   - Target: First Contentful Paint < 1.5s
```

#### 10.3 Browser Testing

**Test in:**
```
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS)
- Chrome Mobile (Android)
```

#### 10.4 SEO Audit

```
Using Yoast SEO:
✓ All pages have unique titles
✓ Meta descriptions set (155-160 chars)
✓ Focus keywords configured
✓ Readability score: Good or higher
✓ SEO score: Good or higher
✓ XML sitemap generated
✓ Robots.txt configured
```

---

### Step 11: Launch Preparation

#### 11.1 Final Checklist

```
✓ Domain DNS propagated
✓ SSL certificate active
✓ All content published
✓ Menus configured
✓ Plugins installed and configured
✓ Contact form working
✓ Analytics installed (if using)
✓ Backup solution active
✓ Security plugin configured
✓ Performance optimized
✓ Mobile-responsive verified
✓ Cross-browser tested
```

#### 11.2 Create Backup

```
UpdraftPlus → Backup Now
- Include: Database, Plugins, Themes, Uploads
- Store backup in: Cloud storage (Dropbox, Google Drive)
```

#### 11.3 Set Up Monitoring

**Google Search Console:**
```
1. Go to https://search.google.com/search-console
2. Add property: neuroliftsolutions.com
3. Verify via DNS or HTML file
4. Submit sitemap: neuroliftsolutions.com/sitemap_index.xml
```

**Cloudflare Analytics:**
```
Already active - check:
- Dashboard → Analytics → Traffic
```

---

### Step 12: Post-Launch Tasks

#### 12.1 Monitor First Week

**Daily checks:**
```
- Site uptime and speed
- Error logs (WordPress + Cloudflare)
- Contact form submissions
- Analytics data
- Security alerts
```

#### 12.2 SEO Submission

```
Submit to search engines:
- Google: Automatic via Search Console
- Bing: https://www.bing.com/webmasters
- Others: Will crawl automatically
```

#### 12.3 Set Update Schedule

```
Weekly:
- Check for plugin updates
- Review security alerts
- Check backup status

Monthly:
- WordPress core updates
- Content updates
- Performance review
- Analytics review
```

---

## 🔄 Maintenance Plan

### Daily
- Monitor uptime
- Check security alerts

### Weekly
- Update plugins
- Review analytics
- Check backups

### Monthly
- WordPress core update
- Full site backup
- Performance audit
- Content review

### Quarterly
- Security audit
- SEO review
- Content strategy review
- Technology updates

---

## 🆘 Troubleshooting

### Common Issues

**White Screen of Death:**
```
1. Access via FTP
2. Rename plugins folder
3. Reload site
4. Identify problematic plugin
5. Fix or remove
```

**404 Errors:**
```
1. WordPress Admin → Settings → Permalinks
2. Click "Save Changes" (even without changes)
3. This regenerates .htaccess
```

**Slow Loading:**
```
1. Clear Cloudflare cache
2. Clear WordPress cache
3. Optimize images
4. Check slow queries
5. Review plugin conflicts
```

**SSL Errors:**
```
1. Verify Cloudflare SSL mode (Full or Full Strict)
2. Install Really Simple SSL plugin
3. Update site URLs in database if needed
```

---

## 📞 Support Resources

### Technical Support
- **WordPress**: https://wordpress.org/support/
- **Cloudflare**: https://community.cloudflare.com/
- **Theme Support**: neuro.edge24@gmail.com

### Documentation
- WordPress Codex: https://codex.wordpress.org/
- Cloudflare Docs: https://developers.cloudflare.com/
- Repository Docs: /docs/cloudflare/CLOUDFLARE_SETUP.md

---

## ✅ Deployment Complete!

Once all steps are completed:

1. ✅ Site is live at neuroliftsolutions.com
2. ✅ All content is published
3. ✅ Cloudflare is optimizing
4. ✅ Security is hardened
5. ✅ Performance is optimized
6. ✅ Monitoring is active

**Welcome to the web, NeuroLift Solutions!** 🚀

---

**Document Version**: 1.0.0  
**Last Updated**: 2024  
**Author**: Joshua Dorsey  
**Website**: neuroliftsolutions.com

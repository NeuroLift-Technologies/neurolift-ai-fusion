# NeuroLift Solutions - Cloudflare Setup Guide

**Complete guide for setting up Cloudflare for neuroliftsolutions.com**

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Cloudflare Workers](#cloudflare-workers)
5. [Cloudflare Pages](#cloudflare-pages)
6. [WordPress Integration](#wordpress-integration)
7. [DNS Configuration](#dns-configuration)
8. [Security Settings](#security-settings)
9. [Performance Optimization](#performance-optimization)
10. [Deployment](#deployment)
11. [Monitoring & Maintenance](#monitoring--maintenance)
12. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers the complete Cloudflare setup for NeuroLift Solutions, including:

- **Cloudflare Workers**: Serverless functions for request handling
- **Cloudflare Pages**: Static site hosting and deployment
- **WordPress Optimization**: Performance and caching for WordPress
- **Security**: Enhanced protection and DDoS mitigation
- **DNS Management**: Domain configuration

### What is Cloudflare?

Cloudflare is a global network that provides:
- Content Delivery Network (CDN)
- DDoS protection
- SSL/TLS encryption
- Serverless computing (Workers)
- Static site hosting (Pages)
- DNS management

---

## Prerequisites

### Required Accounts

1. **Cloudflare Account**
   - Sign up at [cloudflare.com](https://cloudflare.com)
   - Free plan is sufficient to start
   - Email: neuro.edge24@gmail.com

2. **Domain Registration**
   - Domain: neuroliftsolutions.com
   - Registered with: Northwest Registered Agent

3. **WordPress Hosting**
   - Current WordPress site
   - Access to hosting control panel
   - Origin server IP address

### Required Tools

```bash
# Node.js (for Wrangler CLI)
# Install from: https://nodejs.org

# Wrangler CLI (Cloudflare Workers CLI)
npm install -g wrangler

# Python 3 (for utility scripts)
# Install from: https://python.org
pip install requests

# Git (for version control)
# Install from: https://git-scm.com
```

---

## Initial Setup

### Step 1: Add Domain to Cloudflare

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click "Add a Site"
3. Enter: `neuroliftsolutions.com`
4. Select plan (Free is fine to start)
5. Review DNS records (Cloudflare will scan your current DNS)
6. Update nameservers at Northwest Registered Agent

### Step 2: Update Nameservers

Cloudflare will provide two nameservers like:
```
bob.ns.cloudflare.com
lily.ns.cloudflare.com
```

**At Northwest Registered Agent:**
1. Log in to your domain management
2. Find DNS/Nameserver settings
3. Replace current nameservers with Cloudflare's
4. Save changes

**⏱️ Propagation Time:** 24-48 hours (usually faster)

### Step 3: Get API Credentials

1. Go to [API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use template: "Edit Cloudflare Workers"
4. Add permissions:
   - Zone.Zone (Read)
   - Zone.DNS (Edit)
   - Workers Scripts (Edit)
5. Copy the token (you'll only see it once!)

**Save your credentials:**
```bash
# Copy environment template
cp cloudflare/.env.example cloudflare/.env

# Edit .env and add:
# CLOUDFLARE_API_TOKEN=your-token-here
# CLOUDFLARE_ACCOUNT_ID=your-account-id
```

### Step 4: Get Account and Zone IDs

**Account ID:**
- Found in the URL: `https://dash.cloudflare.com/[account-id]/`
- Or on any page, check the right sidebar

**Zone ID:**
- Go to your domain in Cloudflare
- Scroll down in Overview page
- Copy "Zone ID" from API section

---

## Cloudflare Workers

### What are Workers?

Cloudflare Workers are serverless functions that run on Cloudflare's edge network, allowing you to:
- Intercept and modify requests
- Add custom logic
- Optimize performance
- Enhance security

### Available Workers

#### 1. Main Worker (`main-worker.js`)
- General request handling
- Routing logic
- Cache management
- Custom headers

#### 2. WordPress Optimizer (`wordpress-optimizer.js`)
- WordPress-specific caching
- Static asset optimization
- Logged-in user handling
- Performance enhancements

#### 3. Security Worker (`security-worker.js`)
- Rate limiting
- Bot protection
- Security headers
- Threat detection

### Deploy Workers

```bash
# Method 1: Using Wrangler CLI
cd cloudflare/workers

# Login to Wrangler (first time only)
wrangler login

# Deploy main worker
wrangler publish main-worker.js --name neurolift-main-worker

# Deploy WordPress optimizer
wrangler publish wordpress-optimizer.js --name neurolift-wordpress-optimizer

# Deploy security worker
wrangler publish security-worker.js --name neurolift-security-worker

# Method 2: Using deployment script
cd cloudflare/utils
./deploy.sh --workers
```

### Configure Worker Routes

1. Go to Cloudflare Dashboard → Your domain → Workers Routes
2. Add route: `neuroliftsolutions.com/*`
3. Select worker: `neurolift-main-worker`
4. Save

---

## Cloudflare Pages

### What is Cloudflare Pages?

Cloudflare Pages is a JAMstack platform for deploying static sites and frontend applications.

### Use Cases for NeuroLift

1. **Documentation Site**: `docs.neuroliftsolutions.com`
2. **App Interface**: `app.neuroliftsolutions.com` (TOI-OTOI framework)
3. **Landing Pages**: Custom marketing pages
4. **API Documentation**: Developer portal

### Setup Pages Project

#### Option 1: Via Dashboard

1. Go to [Cloudflare Pages](https://dash.cloudflare.com/pages)
2. Click "Create a project"
3. Connect your Git repository
4. Configure build settings:
   - **Project name**: `neurolift-solutions`
   - **Production branch**: `main`
   - **Build command**: (leave empty for static)
   - **Build output directory**: `public`
5. Click "Save and Deploy"

#### Option 2: Via Wrangler

```bash
# Create a Pages project
wrangler pages project create neurolift-solutions

# Deploy
wrangler pages publish public --project-name=neurolift-solutions
```

### Custom Domains for Pages

Add custom domains:
1. Go to your Pages project
2. Click "Custom domains"
3. Add: `docs.neuroliftsolutions.com`
4. Follow DNS setup instructions

---

## WordPress Integration

### Overview

Optimize WordPress performance using Cloudflare's caching and CDN.

### Using Python Helper Script

```bash
cd cloudflare/utils

# Check current status
python3 wordpress-helper.py --domain neuroliftsolutions.com status

# Optimize WordPress settings
python3 wordpress-helper.py --domain neuroliftsolutions.com optimize

# Purge cache
python3 wordpress-helper.py --domain neuroliftsolutions.com purge --all
python3 wordpress-helper.py --domain neuroliftsolutions.com purge --homepage
python3 wordpress-helper.py --domain neuroliftsolutions.com purge --url https://neuroliftsolutions.com/blog/post

# Setup DNS
ORIGIN_IP=your-ip python3 wordpress-helper.py --domain neuroliftsolutions.com dns --ip your-ip
```

### Using Python API Directly

```python
from cloudflare.connector import get_connector, setup_wordpress_site

# Quick setup
results = setup_wordpress_site('neuroliftsolutions.com')
print(results)

# Or manual setup
connector = get_connector()
zones = connector.list_zones()
print(f"Found {len(zones)} zones")
```

### WordPress Plugin Integration

**Recommended Plugin:** Cloudflare for WordPress

1. Install from WordPress plugins
2. Settings → Cloudflare
3. Enter API token
4. Configure caching rules

---

## DNS Configuration

### Basic DNS Setup

```bash
# Using deployment script
ORIGIN_IP=192.0.2.1 ./cloudflare/utils/deploy.sh --dns
```

### Manual DNS Configuration

1. Go to Cloudflare Dashboard → DNS
2. Add records:

| Type  | Name | Content           | Proxy |
|-------|------|-------------------|-------|
| A     | @    | your-hosting-ip   | ✓     |
| A     | www  | your-hosting-ip   | ✓     |
| CNAME | staging | neuroliftsolutions.com | ✓ |

**Proxy Status:**
- ☁️ Proxied (Orange cloud): Traffic goes through Cloudflare
- 🌐 DNS only (Gray cloud): Direct to origin

**Recommendation:** Keep main domain proxied for protection and caching.

### Email DNS Records

If you have email (like Google Workspace):

```
MX    @    ASPMX.L.GOOGLE.COM    Priority: 1
MX    @    ALT1.ASPMX.L.GOOGLE.COM    Priority: 5
MX    @    ALT2.ASPMX.L.GOOGLE.COM    Priority: 5
```

---

## Security Settings

### SSL/TLS Configuration

1. Go to SSL/TLS → Overview
2. Select encryption mode:
   - **Flexible**: Cloudflare ↔ Visitor (HTTPS), Cloudflare ↔ Origin (HTTP)
   - **Full**: HTTPS on both sides (certificate can be self-signed)
   - **Full (Strict)**: HTTPS with valid certificate required
   - **Recommended for WordPress**: Flexible or Full

3. Enable additional features:
   - ✓ Always Use HTTPS
   - ✓ Automatic HTTPS Rewrites
   - ✓ Minimum TLS Version: 1.2

### Security Level

1. Go to Security → Settings
2. Set security level: **Medium** (recommended)
   - Off: No challenges
   - Essentially Off: Only worst threats
   - Low: Few challenges
   - Medium: Balanced (recommended)
   - High: More challenges
   - Under Attack: Maximum protection

### Firewall Rules

Create custom rules:

1. Go to Security → WAF → Firewall rules
2. Create rule:

**Block Bad Bots:**
```
(cf.client.bot and not cf.verified_bot_category eq "Search Engine Crawler")
Action: Block
```

**Rate Limit API:**
```
(http.request.uri.path contains "/api/")
Action: Challenge
```

**Protect Admin:**
```
(http.request.uri.path contains "/wp-admin")
Action: Managed Challenge
```

### DDoS Protection

Enabled automatically. No configuration needed.

### Bot Fight Mode

1. Go to Security → Bots
2. Enable **Bot Fight Mode** (Free plan)
3. Or upgrade for **Super Bot Fight Mode**

---

## Performance Optimization

### Caching Configuration

1. Go to Caching → Configuration
2. Set caching level: **Standard**
3. Browser Cache TTL: **4 hours**

### Page Rules

Create optimization rules:

1. Go to Rules → Page Rules

**Rule 1: Bypass cache for WordPress admin**
- URL: `neuroliftsolutions.com/wp-admin*`
- Settings:
  - Cache Level: Bypass
  - Security Level: High

**Rule 2: Cache static assets**
- URL: `neuroliftsolutions.com/wp-content/*`
- Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 day
  - Browser Cache TTL: 1 day

**Rule 3: Cache homepage**
- URL: `neuroliftsolutions.com/`
- Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 hour

### Auto Minify

1. Go to Speed → Optimization
2. Enable Auto Minify:
   - ✓ JavaScript
   - ✓ CSS
   - ✓ HTML

### Image Optimization

1. Enable **Mirage** (lazy loading)
2. Enable **Polish** (image optimization)
3. Enable **WebP** conversion

### Brotli Compression

1. Go to Speed → Optimization
2. Enable **Brotli**

---

## Deployment

### Complete Deployment

```bash
cd cloudflare/utils

# Check prerequisites
./deploy.sh

# Deploy everything
./deploy.sh --all

# Or deploy individually
./deploy.sh --workers    # Deploy Workers
./deploy.sh --pages      # Setup Pages
./deploy.sh --dns        # Configure DNS
./deploy.sh --optimize   # Optimize WordPress
./deploy.sh --status     # Check status
```

### Manual Verification

After deployment:

1. **DNS Propagation**
   ```bash
   # Check nameservers
   dig NS neuroliftsolutions.com

   # Check A record
   dig A neuroliftsolutions.com
   ```

2. **SSL Certificate**
   - Visit: https://neuroliftsolutions.com
   - Click padlock icon
   - Verify certificate is from Cloudflare

3. **Caching**
   ```bash
   # Check cache headers
   curl -I https://neuroliftsolutions.com
   # Look for: CF-Cache-Status
   ```

4. **Workers**
   - Check for custom headers: `X-Powered-By: NeuroLift Solutions`

---

## Monitoring & Maintenance

### Analytics

1. Go to Analytics → Traffic
2. View metrics:
   - Requests
   - Bandwidth
   - Threats blocked
   - Cache ratio

### Cache Management

**Purge Cache:**

```bash
# Via Python helper
python3 cloudflare/utils/wordpress-helper.py purge --all

# Via Dashboard
# Go to Caching → Configuration → Purge Cache
```

**Best Practices:**
- Purge after WordPress updates
- Purge after theme/plugin changes
- Use selective purge for specific URLs

### Performance Monitoring

Tools:
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

Target metrics:
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Time to Interactive: < 3.5s

### Security Monitoring

1. Go to Security → Overview
2. Review:
   - Threats blocked
   - Attack patterns
   - Top threats

Set up notifications:
1. Go to Notifications
2. Enable alerts for:
   - DDoS attacks
   - SSL certificate expiring
   - High error rates

---

## Troubleshooting

### Common Issues

#### Issue 1: DNS Not Resolving

**Symptoms:** Website not loading, DNS errors

**Solutions:**
1. Check nameservers are updated
2. Wait for DNS propagation (24-48 hours)
3. Clear DNS cache:
   ```bash
   # macOS
   sudo dscacheutil -flushcache

   # Windows
   ipconfig /flushdns

   # Linux
   sudo systemd-resolve --flush-caches
   ```

#### Issue 2: SSL Certificate Errors

**Symptoms:** "Your connection is not private" error

**Solutions:**
1. Check SSL/TLS mode is set correctly
2. Verify origin server has SSL certificate
3. Wait for certificate provisioning (up to 24 hours)
4. Try "Full" instead of "Full (Strict)"

#### Issue 3: WordPress Admin Not Loading

**Symptoms:** Can't access /wp-admin

**Solutions:**
1. Check page rules don't block admin
2. Bypass cache for /wp-admin
3. Temporarily pause Cloudflare:
   - Dashboard → Overview → Pause Cloudflare

#### Issue 4: High Cache Miss Rate

**Symptoms:** Slow performance, low cache hit ratio

**Solutions:**
1. Check cache rules are configured
2. Verify Cache Level is "Standard" or "Cache Everything"
3. Review page rules
4. Check for cookies preventing caching

#### Issue 5: Workers Not Executing

**Symptoms:** Custom headers missing, logic not running

**Solutions:**
1. Check worker is deployed:
   ```bash
   wrangler list
   ```
2. Verify worker routes:
   - Dashboard → Workers → Routes
3. Check worker logs:
   ```bash
   wrangler tail neurolift-main-worker
   ```

### Getting Help

**Cloudflare Support:**
- Community: [community.cloudflare.com](https://community.cloudflare.com)
- Documentation: [developers.cloudflare.com](https://developers.cloudflare.com)
- Email: support@cloudflare.com (paid plans)

**NeuroLift Solutions:**
- Email: neuro.edge24@gmail.com
- Repository: Check documentation in `/docs/cloudflare/`

---

## Next Steps

After completing setup:

1. ✅ Monitor analytics for 1 week
2. ✅ Test WordPress functionality thoroughly
3. ✅ Set up automated backups
4. ✅ Configure email routing (optional)
5. ✅ Plan for TOI-OTOI framework integration
6. ✅ Consider upgrading to Pro plan for enhanced features

---

## Resources

### Official Documentation
- [Cloudflare Docs](https://developers.cloudflare.com)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [Pages Docs](https://developers.cloudflare.com/pages/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)

### Learning Resources
- [Cloudflare Workers Examples](https://developers.cloudflare.com/workers/examples/)
- [Cloudflare Blog](https://blog.cloudflare.com)
- [Cloudflare TV](https://cloudflare.tv)

### Community
- [Discord](https://discord.gg/cloudflaredev)
- [GitHub](https://github.com/cloudflare)
- [Reddit](https://reddit.com/r/CloudFlare)

---

**Document Version:** 1.0.0
**Last Updated:** 2024
**Author:** Joshua Dorsey
**Website:** neuroliftsolutions.com

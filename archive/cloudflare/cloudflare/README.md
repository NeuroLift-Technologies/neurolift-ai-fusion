# NeuroLift Solutions - Cloudflare Integration

**Cloudflare setup for neuroliftsolutions.com WordPress site**

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
npm install -g wrangler
pip install requests

# 2. Configure environment
cp .env.example .env
# Edit .env with your Cloudflare credentials

# 3. Deploy
cd utils
./deploy.sh --all
```

---

## 📁 Directory Structure

```
cloudflare/
├── connector.py              # Python API connector
├── workers/                  # Cloudflare Workers
│   ├── main-worker.js       # Main request handler
│   ├── wordpress-optimizer.js  # WordPress optimization
│   └── security-worker.js   # Security layer
├── config/                   # Configuration files
│   ├── wrangler.toml        # Wrangler CLI config
│   ├── cloudflare-config.yaml  # Cloudflare settings
│   └── pages-config.yaml    # Pages configuration
├── utils/                    # Utility scripts
│   ├── deploy.sh            # Deployment script
│   └── wordpress-helper.py  # WordPress integration
├── .env.example             # Environment template
└── README.md                # This file
```

---

## 🔧 Features

### Cloudflare Workers
- **Main Worker**: Request routing and caching
- **WordPress Optimizer**: WordPress-specific performance optimization
- **Security Worker**: Enhanced security and bot protection

### WordPress Integration
- Cache management
- Performance optimization
- Security headers
- CDN acceleration

### Cloudflare Pages
- Static site hosting
- Serverless functions
- Git integration
- Preview deployments

---

## 📖 Documentation

- **[Complete Setup Guide](../docs/cloudflare/CLOUDFLARE_SETUP.md)** - Comprehensive guide
- **[API Reference](connector.py)** - Python connector documentation
- **[Workers Guide](workers/)** - Worker scripts and usage
- **[Configuration](config/)** - All configuration files

---

## 🛠️ Usage

### Deploy Workers

```bash
# Deploy all workers
cd utils
./deploy.sh --workers

# Or deploy individually with Wrangler
cd workers
wrangler publish main-worker.js --name neurolift-main-worker
```

### Manage WordPress Cache

```bash
# Check status
python3 utils/wordpress-helper.py status

# Optimize settings
python3 utils/wordpress-helper.py optimize

# Purge cache
python3 utils/wordpress-helper.py purge --all
python3 utils/wordpress-helper.py purge --homepage
python3 utils/wordpress-helper.py purge --url https://neuroliftsolutions.com/blog/post
```

### Setup DNS

```bash
# Set ORIGIN_IP and run
ORIGIN_IP=192.0.2.1 ./utils/deploy.sh --dns
```

### Python API Usage

```python
from cloudflare.connector import CloudflareConnector, setup_wordpress_site

# Quick WordPress setup
results = setup_wordpress_site('neuroliftsolutions.com')

# Or use connector directly
connector = CloudflareConnector()
zones = connector.list_zones()
for zone in zones:
    print(f"Zone: {zone['name']}")
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

**Required:**
- `CLOUDFLARE_API_TOKEN` - Your Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID` - Your account ID
- `CLOUDFLARE_ZONE_ID` - Zone ID for neuroliftsolutions.com
- `ORIGIN_IP` - WordPress hosting IP

**Optional:**
- `WORDPRESS_DOMAIN` - Domain (default: neuroliftsolutions.com)
- `WORKER_MAIN` - Main worker name
- `WORKER_WORDPRESS` - WordPress worker name
- `WORKER_SECURITY` - Security worker name

### Get Cloudflare Credentials

1. **API Token:**
   - Go to https://dash.cloudflare.com/profile/api-tokens
   - Create token with permissions: Zone, DNS, Workers

2. **Account ID:**
   - Found in Cloudflare Dashboard URL
   - Or on any zone page (right sidebar)

3. **Zone ID:**
   - Go to your domain in Cloudflare
   - Overview page → API section

---

## 🚦 Deployment Script

The `deploy.sh` script handles all deployment tasks:

```bash
cd utils

# Show help
./deploy.sh --help

# Deploy workers
./deploy.sh --workers

# Setup DNS
ORIGIN_IP=your-ip ./deploy.sh --dns

# Optimize WordPress
./deploy.sh --optimize

# Check status
./deploy.sh --status

# Deploy everything
./deploy.sh --all
```

---

## 🔐 Security

### API Token Security
- ⚠️ Never commit `.env` to version control
- ✅ `.gitignore` includes `.env`
- ✅ Use `.env.example` as template only
- ✅ Rotate tokens regularly

### WordPress Security
- Rate limiting enabled
- Bot protection active
- Security headers applied
- DDoS protection automatic

---

## 🎯 WordPress Optimization

The integration provides:

1. **Caching**
   - Bypass cache for admin/login
   - Aggressive caching for static assets
   - Smart caching for logged-in users

2. **Performance**
   - Image optimization (Polish)
   - Lazy loading (Mirage)
   - Minification (HTML, CSS, JS)
   - Brotli compression

3. **Security**
   - Rate limiting
   - Bot protection
   - Firewall rules
   - SSL/TLS

---

## 📊 Monitoring

### Check Status

```bash
python3 utils/wordpress-helper.py status
```

Output includes:
- Zone status
- DNS records count
- Page rules count
- Security level
- Cache statistics

### Cloudflare Dashboard

Monitor at: https://dash.cloudflare.com

Key metrics:
- Requests per second
- Bandwidth usage
- Threats blocked
- Cache hit ratio

---

## 🐛 Troubleshooting

### Common Issues

**Workers not running:**
```bash
# Check deployment
wrangler list

# View logs
wrangler tail neurolift-main-worker
```

**DNS not resolving:**
```bash
# Check nameservers
dig NS neuroliftsolutions.com

# Check A record
dig A neuroliftsolutions.com
```

**Cache not working:**
```bash
# Check headers
curl -I https://neuroliftsolutions.com
# Look for CF-Cache-Status
```

**Python import errors:**
```bash
# Install requests
pip install requests

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/home/user/neurolift-ai-fusion"
```

### Getting Help

- Documentation: `/docs/cloudflare/CLOUDFLARE_SETUP.md`
- Cloudflare Docs: https://developers.cloudflare.com
- Email: neuro.edge24@gmail.com

---

## 🔄 Workflow

### Development Workflow

1. **Make changes** to workers or config
2. **Test locally** (if using wrangler dev)
3. **Deploy** using deployment script
4. **Verify** using status checks
5. **Monitor** via Cloudflare Dashboard

### Production Workflow

1. **Deploy** to staging first (if configured)
2. **Test** thoroughly
3. **Deploy** to production
4. **Monitor** analytics and errors
5. **Optimize** based on metrics

---

## 📈 Performance Tips

1. **Enable Auto Minify** - Reduces file sizes
2. **Use Cache Everything** - For static pages
3. **Enable Brotli** - Better compression than gzip
4. **Optimize Images** - Enable Polish and WebP
5. **Use Workers** - For custom logic at the edge
6. **Monitor Cache Ratio** - Aim for >80%

---

## 🌐 TOI-OTOI Framework Integration

Future integration with the TOI-OTOI framework:

- **API Gateway**: Route AI requests through Workers
- **Edge Computing**: Run Avatar/Aide logic at edge
- **Real-time Updates**: WebSocket support
- **Data Privacy**: Process data at edge, not origin

See main repository documentation for TOI-OTOI details.

---

## 📝 To-Do

- [ ] Set up Cloudflare KV for session storage
- [ ] Implement Durable Objects for rate limiting
- [ ] Create R2 bucket for asset storage
- [ ] Set up D1 database for analytics
- [ ] Configure email routing
- [ ] Add WebSocket support for real-time features

---

## 📞 Support

**NeuroLift Solutions**
- Website: neuroliftsolutions.com
- Email: neuro.edge24@gmail.com
- GitHub: Check repository issues

**Cloudflare**
- Dashboard: https://dash.cloudflare.com
- Documentation: https://developers.cloudflare.com
- Community: https://community.cloudflare.com

---

## 📄 License

Private repository - All rights reserved

---

## 🙏 Acknowledgments

Built for NeuroLift Solutions by Joshua Dorsey

Powered by:
- Cloudflare Workers
- Cloudflare Pages
- WordPress
- Python & JavaScript

---

**Version:** 1.0.0
**Last Updated:** 2024
**Status:** ✅ Production Ready

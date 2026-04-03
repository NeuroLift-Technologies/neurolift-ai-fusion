#!/bin/bash

###############################################################################
# NeuroLift Solutions - Cloudflare Deployment Script
###############################################################################
#
# Deploy Cloudflare Workers and configure services
# Website: neuroliftsolutions.com
#
# Usage:
#   ./deploy.sh [options]
#
# Options:
#   --workers     Deploy Cloudflare Workers
#   --pages       Deploy Cloudflare Pages
#   --dns         Setup DNS records
#   --optimize    Apply WordPress optimizations
#   --all         Deploy everything
#   --help        Show this help message
#
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLOUDFLARE_DIR="$(dirname "$SCRIPT_DIR")"
WORKERS_DIR="$CLOUDFLARE_DIR/workers"
CONFIG_DIR="$CLOUDFLARE_DIR/config"

# Functions
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check for wrangler
    if command -v wrangler &> /dev/null; then
        print_success "Wrangler CLI found: $(wrangler --version)"
    else
        print_error "Wrangler CLI not found"
        print_info "Install with: npm install -g wrangler"
        exit 1
    fi

    # Check for Python
    if command -v python3 &> /dev/null; then
        print_success "Python found: $(python3 --version)"
    else
        print_warning "Python not found (optional for utilities)"
    fi

    # Check environment variables
    if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
        print_warning "CLOUDFLARE_API_TOKEN not set"
        print_info "Set with: export CLOUDFLARE_API_TOKEN=your-token"
    else
        print_success "CLOUDFLARE_API_TOKEN is set"
    fi

    if [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
        print_warning "CLOUDFLARE_ACCOUNT_ID not set"
        print_info "Set with: export CLOUDFLARE_ACCOUNT_ID=your-account-id"
    else
        print_success "CLOUDFLARE_ACCOUNT_ID is set"
    fi
}

# Deploy Workers
deploy_workers() {
    print_header "Deploying Cloudflare Workers"

    cd "$WORKERS_DIR"

    # Deploy main worker
    print_info "Deploying main-worker.js..."
    if wrangler publish main-worker.js --name neurolift-main-worker 2>/dev/null; then
        print_success "main-worker deployed"
    else
        print_warning "main-worker deployment skipped (configure wrangler.toml first)"
    fi

    # Deploy WordPress optimizer
    print_info "Deploying wordpress-optimizer.js..."
    if wrangler publish wordpress-optimizer.js --name neurolift-wordpress-optimizer 2>/dev/null; then
        print_success "wordpress-optimizer deployed"
    else
        print_warning "wordpress-optimizer deployment skipped"
    fi

    # Deploy security worker
    print_info "Deploying security-worker.js..."
    if wrangler publish security-worker.js --name neurolift-security-worker 2>/dev/null; then
        print_success "security-worker deployed"
    else
        print_warning "security-worker deployment skipped"
    fi

    cd - > /dev/null
}

# Setup DNS
setup_dns() {
    print_header "Setting Up DNS Records"

    if command -v python3 &> /dev/null; then
        if [ -z "$ORIGIN_IP" ]; then
            print_warning "ORIGIN_IP not set"
            print_info "Usage: ORIGIN_IP=your-ip ./deploy.sh --dns"
        else
            python3 "$SCRIPT_DIR/wordpress-helper.py" --domain neuroliftsolutions.com dns --ip "$ORIGIN_IP"
        fi
    else
        print_error "Python3 required for DNS setup"
    fi
}

# Optimize WordPress
optimize_wordpress() {
    print_header "Optimizing WordPress Configuration"

    if command -v python3 &> /dev/null; then
        python3 "$SCRIPT_DIR/wordpress-helper.py" --domain neuroliftsolutions.com optimize
    else
        print_error "Python3 required for WordPress optimization"
    fi
}

# Check status
check_status() {
    print_header "Checking WordPress + Cloudflare Status"

    if command -v python3 &> /dev/null; then
        python3 "$SCRIPT_DIR/wordpress-helper.py" --domain neuroliftsolutions.com status
    else
        print_error "Python3 required for status check"
    fi
}

# Deploy Pages
deploy_pages() {
    print_header "Deploying Cloudflare Pages"

    print_info "Pages deployment is typically done via git push"
    print_info "Connect your repository at: https://dash.cloudflare.com/pages"
    print_warning "Manual setup required for first deployment"
}

# Show help
show_help() {
    cat << EOF
NeuroLift Solutions - Cloudflare Deployment Script
===================================================

Deploy Cloudflare Workers and configure services for neuroliftsolutions.com

Usage:
    ./deploy.sh [options]

Options:
    --workers       Deploy Cloudflare Workers
    --pages         Deploy Cloudflare Pages
    --dns           Setup DNS records (requires ORIGIN_IP env var)
    --optimize      Apply WordPress optimizations
    --status        Check current status
    --all           Deploy everything
    --help          Show this help message

Environment Variables:
    CLOUDFLARE_API_TOKEN    Your Cloudflare API token (required)
    CLOUDFLARE_ACCOUNT_ID   Your Cloudflare account ID (required)
    ORIGIN_IP               Origin server IP (required for --dns)

Examples:
    # Deploy all workers
    ./deploy.sh --workers

    # Setup DNS
    ORIGIN_IP=192.0.2.1 ./deploy.sh --dns

    # Optimize WordPress
    ./deploy.sh --optimize

    # Check status
    ./deploy.sh --status

    # Deploy everything
    ./deploy.sh --all

Prerequisites:
    - Wrangler CLI: npm install -g wrangler
    - Python 3 (for utilities)
    - Cloudflare API token
    - Cloudflare account ID

For more information:
    - Website: neuroliftsolutions.com
    - Cloudflare Docs: https://developers.cloudflare.com
    - Wrangler Docs: https://developers.cloudflare.com/workers/wrangler/

EOF
}

# Main execution
main() {
    print_header "NeuroLift Solutions - Cloudflare Deployment"

    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    # Parse arguments
    while [ $# -gt 0 ]; do
        case $1 in
            --workers)
                check_prerequisites
                deploy_workers
                ;;
            --pages)
                check_prerequisites
                deploy_pages
                ;;
            --dns)
                check_prerequisites
                setup_dns
                ;;
            --optimize)
                check_prerequisites
                optimize_wordpress
                ;;
            --status)
                check_prerequisites
                check_status
                ;;
            --all)
                check_prerequisites
                deploy_workers
                deploy_pages
                setup_dns
                optimize_wordpress
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
        shift
    done

    print_header "Deployment Complete"
    print_success "All tasks completed successfully!"
    print_info "Check the output above for any warnings or errors"
}

# Run main function
main "$@"

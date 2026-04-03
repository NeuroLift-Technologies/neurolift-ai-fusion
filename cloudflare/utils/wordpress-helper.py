"""
NeuroLift Solutions - WordPress Integration Helper
===================================================

Utilities for integrating WordPress with Cloudflare
Handles cache purging, optimization, and WordPress-specific tasks

Author: Joshua Dorsey
Website: neuroliftsolutions.com
"""

import sys
import os
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connector import CloudflareConnector, WordPressCloudflareIntegration


class WordPressHelper:
    """
    Helper class for WordPress + Cloudflare operations.
    """

    def __init__(self, domain: str = 'neuroliftsolutions.com'):
        """
        Initialize WordPress helper.

        Args:
            domain: WordPress domain
        """
        self.domain = domain
        self.connector = CloudflareConnector()
        self.wp_integration = WordPressCloudflareIntegration(self.connector, domain)

    def purge_post_cache(self, post_id: int, post_url: str) -> bool:
        """
        Purge cache for a specific WordPress post.

        Args:
            post_id: WordPress post ID
            post_url: Full URL of the post

        Returns:
            Success status
        """
        if not self.wp_integration.zone_id:
            print("Error: Zone ID not found")
            return False

        try:
            # Purge specific post URL
            urls_to_purge = [
                post_url,
                f"{post_url}/",
                f"{post_url}?",
            ]

            success = self.connector.purge_cache(
                self.wp_integration.zone_id,
                files=urls_to_purge
            )

            if success:
                print(f"✓ Cache purged for post {post_id}: {post_url}")
            return success

        except Exception as e:
            print(f"Error purging cache: {e}")
            return False

    def purge_homepage_cache(self) -> bool:
        """
        Purge cache for the homepage.

        Returns:
            Success status
        """
        if not self.wp_integration.zone_id:
            print("Error: Zone ID not found")
            return False

        try:
            urls = [
                f"https://{self.domain}/",
                f"https://{self.domain}",
                f"https://www.{self.domain}/",
                f"https://www.{self.domain}",
            ]

            success = self.connector.purge_cache(
                self.wp_integration.zone_id,
                files=urls
            )

            if success:
                print(f"✓ Homepage cache purged")
            return success

        except Exception as e:
            print(f"Error purging homepage cache: {e}")
            return False

    def purge_all_cache(self) -> bool:
        """
        Purge all cached content for the site.

        Returns:
            Success status
        """
        if not self.wp_integration.zone_id:
            print("Error: Zone ID not found")
            return False

        try:
            success = self.connector.purge_cache(
                self.wp_integration.zone_id,
                purge_everything=True
            )

            if success:
                print(f"✓ All cache purged for {self.domain}")
            return success

        except Exception as e:
            print(f"Error purging all cache: {e}")
            return False

    def setup_wordpress_dns(self, origin_ip: str) -> Dict:
        """
        Set up DNS records for WordPress site.

        Args:
            origin_ip: IP address of WordPress hosting

        Returns:
            Created DNS records
        """
        if not self.wp_integration.zone_id:
            print("Error: Zone ID not found")
            return {}

        records = {}

        try:
            # Create root domain A record
            root_record = self.connector.create_dns_record(
                self.wp_integration.zone_id,
                'A',
                self.domain,
                origin_ip,
                proxied=True
            )
            records['root'] = root_record
            print(f"✓ Created A record: {self.domain} -> {origin_ip}")

            # Create www CNAME record
            www_record = self.connector.create_dns_record(
                self.wp_integration.zone_id,
                'A',
                f'www.{self.domain}',
                origin_ip,
                proxied=True
            )
            records['www'] = www_record
            print(f"✓ Created A record: www.{self.domain} -> {origin_ip}")

        except Exception as e:
            print(f"Error setting up DNS: {e}")

        return records

    def get_cache_status(self) -> Dict:
        """
        Get cache statistics and status.

        Returns:
            Cache status information
        """
        if not self.wp_integration.zone_id:
            return {'error': 'Zone ID not available'}

        try:
            # Get zone details which include cache info
            zone = self.connector.get_zone_details(self.wp_integration.zone_id)
            return {
                'domain': self.domain,
                'zone_id': self.wp_integration.zone_id,
                'status': zone.get('status'),
                'name_servers': zone.get('name_servers', []),
            }

        except Exception as e:
            return {'error': str(e)}

    def optimize_wordpress_settings(self) -> Dict:
        """
        Apply all WordPress optimizations.

        Returns:
            Results of optimizations
        """
        print(f"\n🚀 Optimizing WordPress site: {self.domain}")
        print("=" * 60)

        results = {
            'optimization': self.wp_integration.setup_wordpress_optimization(),
            'page_rules': self.wp_integration.create_wordpress_page_rules(),
        }

        print("\n✓ WordPress optimization complete!")
        return results

    def check_wordpress_status(self) -> Dict:
        """
        Check the status of WordPress + Cloudflare integration.

        Returns:
            Status information
        """
        print(f"\n🔍 Checking WordPress status: {self.domain}")
        print("=" * 60)

        status = {
            'domain': self.domain,
            'zone_id': self.wp_integration.zone_id,
        }

        if not self.wp_integration.zone_id:
            status['error'] = 'Zone not found in Cloudflare'
            return status

        try:
            # Get zone details
            zone = self.connector.get_zone_details(self.wp_integration.zone_id)
            status['zone_status'] = zone.get('status')
            status['name_servers'] = zone.get('name_servers', [])

            # Get DNS records
            dns_records = self.connector.list_dns_records(self.wp_integration.zone_id)
            status['dns_records'] = len(dns_records)

            # Get page rules
            page_rules = self.connector.list_page_rules(self.wp_integration.zone_id)
            status['page_rules'] = len(page_rules)

            # Get security level
            security = self.connector.get_security_level(self.wp_integration.zone_id)
            status['security_level'] = security

            print(f"\n✓ Zone Status: {status['zone_status']}")
            print(f"✓ DNS Records: {status['dns_records']}")
            print(f"✓ Page Rules: {status['page_rules']}")
            print(f"✓ Security Level: {status['security_level']}")

        except Exception as e:
            status['error'] = str(e)
            print(f"\n✗ Error: {e}")

        return status


def main():
    """Main function for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='WordPress + Cloudflare Integration Helper'
    )
    parser.add_argument(
        '--domain',
        default='neuroliftsolutions.com',
        help='WordPress domain'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Status command
    subparsers.add_parser('status', help='Check WordPress + Cloudflare status')

    # Optimize command
    subparsers.add_parser('optimize', help='Apply WordPress optimizations')

    # Purge commands
    purge_parser = subparsers.add_parser('purge', help='Purge cache')
    purge_parser.add_argument('--all', action='store_true', help='Purge all cache')
    purge_parser.add_argument('--homepage', action='store_true', help='Purge homepage')
    purge_parser.add_argument('--url', help='Purge specific URL')

    # DNS command
    dns_parser = subparsers.add_parser('dns', help='Setup DNS records')
    dns_parser.add_argument('--ip', required=True, help='Origin server IP')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize helper
    helper = WordPressHelper(args.domain)

    # Execute command
    if args.command == 'status':
        helper.check_wordpress_status()

    elif args.command == 'optimize':
        helper.optimize_wordpress_settings()

    elif args.command == 'purge':
        if args.all:
            helper.purge_all_cache()
        elif args.homepage:
            helper.purge_homepage_cache()
        elif args.url:
            helper.purge_post_cache(0, args.url)
        else:
            print("Error: Specify --all, --homepage, or --url")

    elif args.command == 'dns':
        helper.setup_wordpress_dns(args.ip)


if __name__ == '__main__':
    main()

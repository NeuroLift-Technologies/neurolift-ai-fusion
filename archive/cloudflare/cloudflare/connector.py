"""
NeuroLift Solutions - Cloudflare API Connector
==============================================

A comprehensive connector for Cloudflare API integration, supporting:
- Cloudflare Workers management
- DNS management
- Page Rules
- WordPress site integration
- Security and performance optimization

Author: Joshua Dorsey
Website: neuroliftsolutions.com
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class CloudflareConnector:
    """
    Main connector class for Cloudflare API integration.
    Provides methods for managing Cloudflare resources.
    """

    def __init__(self, api_token: Optional[str] = None, account_id: Optional[str] = None):
        """
        Initialize the Cloudflare connector.

        Args:
            api_token: Cloudflare API token (or set CLOUDFLARE_API_TOKEN env var)
            account_id: Cloudflare account ID (or set CLOUDFLARE_ACCOUNT_ID env var)
        """
        self.api_token = api_token or os.getenv('CLOUDFLARE_API_TOKEN')
        self.account_id = account_id or os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.base_url = 'https://api.cloudflare.com/client/v4'

        if not self.api_token:
            raise ValueError("Cloudflare API token is required. Set CLOUDFLARE_API_TOKEN environment variable.")

        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the Cloudflare API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request payload

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Cloudflare API Error: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    # =====================
    # Zone Management
    # =====================

    def list_zones(self) -> List[Dict]:
        """
        List all zones (domains) in the account.

        Returns:
            List of zone objects
        """
        response = self._make_request('GET', '/zones')
        return response.get('result', [])

    def get_zone_id(self, domain: str) -> Optional[str]:
        """
        Get the zone ID for a specific domain.

        Args:
            domain: Domain name (e.g., 'neuroliftsolutions.com')

        Returns:
            Zone ID or None if not found
        """
        zones = self.list_zones()
        for zone in zones:
            if zone.get('name') == domain:
                return zone.get('id')
        return None

    def get_zone_details(self, zone_id: str) -> Dict:
        """
        Get detailed information about a zone.

        Args:
            zone_id: Zone identifier

        Returns:
            Zone details
        """
        response = self._make_request('GET', f'/zones/{zone_id}')
        return response.get('result', {})

    # =====================
    # DNS Management
    # =====================

    def list_dns_records(self, zone_id: str) -> List[Dict]:
        """
        List all DNS records for a zone.

        Args:
            zone_id: Zone identifier

        Returns:
            List of DNS records
        """
        response = self._make_request('GET', f'/zones/{zone_id}/dns_records')
        return response.get('result', [])

    def create_dns_record(self, zone_id: str, record_type: str, name: str,
                         content: str, ttl: int = 1, proxied: bool = True) -> Dict:
        """
        Create a new DNS record.

        Args:
            zone_id: Zone identifier
            record_type: Record type (A, AAAA, CNAME, TXT, etc.)
            name: DNS record name
            content: Record content (IP address, target, etc.)
            ttl: Time to live (1 = auto)
            proxied: Whether to proxy through Cloudflare

        Returns:
            Created DNS record
        """
        data = {
            'type': record_type,
            'name': name,
            'content': content,
            'ttl': ttl,
            'proxied': proxied
        }
        response = self._make_request('POST', f'/zones/{zone_id}/dns_records', data)
        return response.get('result', {})

    def update_dns_record(self, zone_id: str, record_id: str, **kwargs) -> Dict:
        """
        Update an existing DNS record.

        Args:
            zone_id: Zone identifier
            record_id: DNS record identifier
            **kwargs: Fields to update

        Returns:
            Updated DNS record
        """
        response = self._make_request('PUT', f'/zones/{zone_id}/dns_records/{record_id}', kwargs)
        return response.get('result', {})

    def delete_dns_record(self, zone_id: str, record_id: str) -> bool:
        """
        Delete a DNS record.

        Args:
            zone_id: Zone identifier
            record_id: DNS record identifier

        Returns:
            Success status
        """
        response = self._make_request('DELETE', f'/zones/{zone_id}/dns_records/{record_id}')
        return response.get('success', False)

    # =====================
    # Workers Management
    # =====================

    def list_workers(self) -> List[Dict]:
        """
        List all Cloudflare Workers scripts.

        Returns:
            List of worker scripts
        """
        if not self.account_id:
            raise ValueError("Account ID is required for Workers management")

        response = self._make_request('GET', f'/accounts/{self.account_id}/workers/scripts')
        return response.get('result', [])

    def upload_worker(self, script_name: str, script_content: str,
                     bindings: Optional[List[Dict]] = None) -> Dict:
        """
        Upload a Cloudflare Worker script.

        Args:
            script_name: Name of the worker script
            script_content: JavaScript code for the worker
            bindings: Worker bindings (KV, Durable Objects, etc.)

        Returns:
            Upload result
        """
        if not self.account_id:
            raise ValueError("Account ID is required for Workers management")

        # Prepare metadata
        metadata = {
            'body_part': 'script',
            'bindings': bindings or []
        }

        # For Workers API, we need multipart/form-data
        files = {
            'metadata': (None, json.dumps(metadata), 'application/json'),
            'script': (None, script_content, 'application/javascript')
        }

        url = f"{self.base_url}/accounts/{self.account_id}/workers/scripts/{script_name}"
        headers = {'Authorization': f'Bearer {self.api_token}'}

        response = requests.put(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()

    def delete_worker(self, script_name: str) -> bool:
        """
        Delete a Cloudflare Worker script.

        Args:
            script_name: Name of the worker script

        Returns:
            Success status
        """
        if not self.account_id:
            raise ValueError("Account ID is required for Workers management")

        response = self._make_request('DELETE',
                                      f'/accounts/{self.account_id}/workers/scripts/{script_name}')
        return response.get('success', False)

    # =====================
    # Page Rules
    # =====================

    def list_page_rules(self, zone_id: str) -> List[Dict]:
        """
        List all page rules for a zone.

        Args:
            zone_id: Zone identifier

        Returns:
            List of page rules
        """
        response = self._make_request('GET', f'/zones/{zone_id}/pagerules')
        return response.get('result', [])

    def create_page_rule(self, zone_id: str, targets: List[Dict],
                        actions: List[Dict], priority: int = 1) -> Dict:
        """
        Create a new page rule.

        Args:
            zone_id: Zone identifier
            targets: List of target patterns
            actions: List of actions to apply
            priority: Rule priority

        Returns:
            Created page rule
        """
        data = {
            'targets': targets,
            'actions': actions,
            'priority': priority,
            'status': 'active'
        }
        response = self._make_request('POST', f'/zones/{zone_id}/pagerules', data)
        return response.get('result', {})

    # =====================
    # Security & Performance
    # =====================

    def get_security_level(self, zone_id: str) -> str:
        """
        Get the security level for a zone.

        Args:
            zone_id: Zone identifier

        Returns:
            Security level (off, essentially_off, low, medium, high, under_attack)
        """
        response = self._make_request('GET', f'/zones/{zone_id}/settings/security_level')
        return response.get('result', {}).get('value', 'unknown')

    def set_security_level(self, zone_id: str, level: str) -> Dict:
        """
        Set the security level for a zone.

        Args:
            zone_id: Zone identifier
            level: Security level (off, essentially_off, low, medium, high, under_attack)

        Returns:
            Updated setting
        """
        data = {'value': level}
        response = self._make_request('PATCH', f'/zones/{zone_id}/settings/security_level', data)
        return response.get('result', {})

    def enable_ssl(self, zone_id: str, mode: str = 'flexible') -> Dict:
        """
        Enable SSL for a zone.

        Args:
            zone_id: Zone identifier
            mode: SSL mode (off, flexible, full, strict)

        Returns:
            Updated SSL setting
        """
        data = {'value': mode}
        response = self._make_request('PATCH', f'/zones/{zone_id}/settings/ssl', data)
        return response.get('result', {})

    def purge_cache(self, zone_id: str, purge_everything: bool = False,
                   files: Optional[List[str]] = None) -> bool:
        """
        Purge cached content.

        Args:
            zone_id: Zone identifier
            purge_everything: Purge all cached content
            files: List of specific files to purge

        Returns:
            Success status
        """
        data = {}
        if purge_everything:
            data['purge_everything'] = True
        elif files:
            data['files'] = files
        else:
            raise ValueError("Must specify either purge_everything=True or provide files list")

        response = self._make_request('POST', f'/zones/{zone_id}/purge_cache', data)
        return response.get('success', False)

    # =====================
    # Analytics
    # =====================

    def get_analytics(self, zone_id: str, since: Optional[str] = None,
                     until: Optional[str] = None) -> Dict:
        """
        Get analytics data for a zone.

        Args:
            zone_id: Zone identifier
            since: Start time (ISO 8601 format)
            until: End time (ISO 8601 format)

        Returns:
            Analytics data
        """
        params = {}
        if since:
            params['since'] = since
        if until:
            params['until'] = until

        response = self._make_request('GET', f'/zones/{zone_id}/analytics/dashboard', params)
        return response.get('result', {})


# =====================
# WordPress Integration Helper
# =====================

class WordPressCloudflareIntegration:
    """
    Helper class for WordPress-specific Cloudflare integration.
    Optimized for neuroliftsolutions.com WordPress site.
    """

    def __init__(self, connector: CloudflareConnector, domain: str = 'neuroliftsolutions.com'):
        """
        Initialize WordPress integration.

        Args:
            connector: CloudflareConnector instance
            domain: WordPress domain
        """
        self.connector = connector
        self.domain = domain
        self.zone_id = connector.get_zone_id(domain)

        if not self.zone_id:
            print(f"Warning: Zone ID not found for {domain}. Some features may not work.")

    def setup_wordpress_optimization(self) -> Dict[str, Any]:
        """
        Apply WordPress-optimized Cloudflare settings.

        Returns:
            Results of applied optimizations
        """
        if not self.zone_id:
            return {'error': 'Zone ID not available'}

        results = {}

        # Enable SSL
        try:
            results['ssl'] = self.connector.enable_ssl(self.zone_id, 'flexible')
        except Exception as e:
            results['ssl_error'] = str(e)

        # Set security level to medium
        try:
            results['security'] = self.connector.set_security_level(self.zone_id, 'medium')
        except Exception as e:
            results['security_error'] = str(e)

        return results

    def create_wordpress_page_rules(self) -> List[Dict]:
        """
        Create WordPress-specific page rules for caching and security.

        Returns:
            List of created page rules
        """
        if not self.zone_id:
            return []

        rules = []

        # Skip caching for WordPress admin
        try:
            admin_rule = self.connector.create_page_rule(
                self.zone_id,
                targets=[{'target': 'url', 'constraint': {'operator': 'matches',
                         'value': f'{self.domain}/wp-admin*'}}],
                actions=[{'id': 'cache_level', 'value': 'bypass'}],
                priority=1
            )
            rules.append(admin_rule)
        except Exception as e:
            print(f"Error creating admin rule: {e}")

        # Cache static assets
        try:
            static_rule = self.connector.create_page_rule(
                self.zone_id,
                targets=[{'target': 'url', 'constraint': {'operator': 'matches',
                         'value': f'{self.domain}/wp-content/*'}}],
                actions=[
                    {'id': 'cache_level', 'value': 'cache_everything'},
                    {'id': 'edge_cache_ttl', 'value': 86400}  # 24 hours
                ],
                priority=2
            )
            rules.append(static_rule)
        except Exception as e:
            print(f"Error creating static assets rule: {e}")

        return rules


# =====================
# Convenience Functions
# =====================

def get_connector(api_token: Optional[str] = None,
                 account_id: Optional[str] = None) -> CloudflareConnector:
    """
    Get a configured CloudflareConnector instance.

    Args:
        api_token: Cloudflare API token
        account_id: Cloudflare account ID

    Returns:
        CloudflareConnector instance
    """
    return CloudflareConnector(api_token, account_id)


def setup_wordpress_site(domain: str = 'neuroliftsolutions.com') -> Dict:
    """
    Quick setup for WordPress site with optimal Cloudflare settings.

    Args:
        domain: WordPress domain

    Returns:
        Setup results
    """
    connector = get_connector()
    wp_integration = WordPressCloudflareIntegration(connector, domain)

    results = {
        'domain': domain,
        'optimization': wp_integration.setup_wordpress_optimization(),
        'page_rules': wp_integration.create_wordpress_page_rules()
    }

    return results


if __name__ == '__main__':
    # Example usage
    print("NeuroLift Solutions - Cloudflare Connector")
    print("=" * 50)

    try:
        connector = get_connector()

        # List zones
        zones = connector.list_zones()
        print(f"\nFound {len(zones)} zone(s):")
        for zone in zones:
            print(f"  - {zone['name']} (ID: {zone['id']})")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease set the following environment variables:")
        print("  CLOUDFLARE_API_TOKEN - Your Cloudflare API token")
        print("  CLOUDFLARE_ACCOUNT_ID - Your Cloudflare account ID")

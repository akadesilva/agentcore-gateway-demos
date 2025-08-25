#!/usr/bin/env python3
"""
SharePoint API Client - Query SharePoint sites using access tokens
"""

import requests
import json
import argparse
import sys
from datetime import datetime


class SharePointClient:
    """Client for interacting with SharePoint via Microsoft Graph API"""
    
    def __init__(self, access_token, verbose=False):
        self.access_token = access_token
        self.verbose = verbose
        self.base_url = "https://graph.microsoft.com/v1.0"
        
        # Set up headers
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint, method='GET', params=None):
        """Make authenticated request to Microsoft Graph"""
        url = f"{self.base_url}/{endpoint}"
        
        if self.verbose:
            print(f"Making {method} request to: {url}")
            if params:
                print(f"Parameters: {params}")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if self.verbose:
                print(f"Response status: {response.status_code}")
                print(f"Response headers: {dict(response.headers)}")
            
            # Handle different response codes
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ Authentication failed - token may be expired or invalid")
                return None
            elif response.status_code == 403:
                print("❌ Access denied - insufficient permissions")
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        print(f"Error: {error_data['error'].get('message', 'Unknown error')}")
                except:
                    pass
                return None
            else:
                print(f"❌ Request failed with status {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error response: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Error response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def list_sites(self, search_query=None, limit=25):
        """List SharePoint sites"""
        print("🔍 Querying SharePoint sites...")
        
        if search_query:
            # Search for specific sites
            endpoint = f"sites?search={search_query}"
            print(f"Searching for sites matching: '{search_query}'")
        else:
            # List all sites (or use a broad search)
            endpoint = "sites?search=*"
            print("Listing all accessible sites")
        
        # Add limit parameter
        params = {'$top': limit}
        
        result = self._make_request(endpoint, params=params)
        
        if result and 'value' in result:
            sites = result['value']
            
            print(f"\n✅ Found {len(sites)} sites:")
            print("=" * 80)
            
            for i, site in enumerate(sites, 1):
                print(f"\n{i}. {site.get('displayName', 'Unknown Site')}")
                print(f"   ID: {site.get('id', 'N/A')}")
                print(f"   URL: {site.get('webUrl', 'N/A')}")
                print(f"   Description: {site.get('description', 'No description')}")
                
                if 'createdDateTime' in site:
                    created = datetime.fromisoformat(site['createdDateTime'].replace('Z', '+00:00'))
                    print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                
                if 'lastModifiedDateTime' in site:
                    modified = datetime.fromisoformat(site['lastModifiedDateTime'].replace('Z', '+00:00'))
                    print(f"   Modified: {modified.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Show pagination info if available
            if '@odata.nextLink' in result:
                print(f"\n💡 More results available (showing first {limit})")
            
            if self.verbose:
                print(f"\nFull API Response:")
                print("-" * 40)
                print(json.dumps(result, indent=2))
            
            return sites
        else:
            print("❌ No sites found or request failed")
            return []
    
    def get_site_details(self, site_id):
        """Get detailed information about a specific site"""
        print(f"🔍 Getting details for site: {site_id}")
        
        endpoint = f"sites/{site_id}"
        result = self._make_request(endpoint)
        
        if result:
            print(f"\n✅ Site Details:")
            print("=" * 50)
            print(f"Name: {result.get('displayName', 'N/A')}")
            print(f"ID: {result.get('id', 'N/A')}")
            print(f"URL: {result.get('webUrl', 'N/A')}")
            print(f"Description: {result.get('description', 'No description')}")
            
            if 'createdDateTime' in result:
                created = datetime.fromisoformat(result['createdDateTime'].replace('Z', '+00:00'))
                print(f"Created: {created.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            if self.verbose:
                print(f"\nFull Site Details:")
                print("-" * 40)
                print(json.dumps(result, indent=2))
            
            return result
        else:
            print("❌ Failed to get site details")
            return None
    
    def test_token(self):
        """Test if the access token is valid"""
        print("🔍 Testing access token...")
        
        # For Client Credentials tokens, test with sites endpoint
        # /me only works with delegated (user) tokens
        result = self._make_request("sites?$top=1")
        
        if result:
            print("✅ Access token is valid for SharePoint access!")
            print("🔑 Token type: Application token (Client Credentials)")
            
            if 'value' in result and len(result['value']) > 0:
                site_count = len(result['value'])
                print(f"📊 Can access SharePoint sites (found at least {site_count})")
                
                # Show first site as example
                first_site = result['value'][0]
                print(f"📁 Example accessible site: {first_site.get('displayName', 'Unknown')}")
            else:
                print("📊 Token is valid but no sites found (may need different permissions)")
            
            return True
        else:
            print("❌ Access token is invalid, expired, or lacks SharePoint permissions")
            print("💡 For Client Credentials tokens:")
            print("   • Ensure 'Sites.Read.All' application permission is granted")
            print("   • Ensure admin consent is provided")
            print("   • Token should be for https://graph.microsoft.com/.default scope")
            return False


def main():
    parser = argparse.ArgumentParser(description='SharePoint API Client')
    parser.add_argument('--token', required=True, help='Access token from OAuth flow')
    parser.add_argument('--action', choices=['list-sites', 'site-details', 'test-token'], 
                       default='list-sites', help='Action to perform')
    parser.add_argument('--site-id', help='Site ID for site-details action')
    parser.add_argument('--search', help='Search query for sites')
    parser.add_argument('--limit', type=int, default=25, help='Maximum number of sites to return')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize client
    client = SharePointClient(args.token, verbose=args.verbose)
    
    try:
        if args.action == 'test-token':
            success = client.test_token()
            return 0 if success else 1
            
        elif args.action == 'list-sites':
            sites = client.list_sites(search_query=args.search, limit=args.limit)
            return 0 if sites else 1
            
        elif args.action == 'site-details':
            if not args.site_id:
                print("Error: --site-id is required for site-details action")
                return 1
            
            site = client.get_site_details(args.site_id)
            return 0 if site else 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

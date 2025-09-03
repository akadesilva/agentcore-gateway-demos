#!/usr/bin/env python3
"""
OAuth Tester - A CLI tool for testing various OAuth 2.0 flows
"""

import argparse
import sys
from providers.microsoft import MicrosoftOAuthProvider
from providers.salesforce import SalesforceOAuthProvider
from flows.auth_code import AuthorizationCodeFlow
from flows.client_credentials import ClientCredentialsFlow
from utils.discovery import analyze_client_capabilities


def main():
    parser = argparse.ArgumentParser(description='OAuth 2.0 Flow Tester')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Discovery command
    discovery_parser = subparsers.add_parser('discover', help='Discover OAuth capabilities')
    discovery_parser.add_argument('--provider', required=True, choices=['microsoft', 'salesforce'], 
                                 help='OAuth provider')
    discovery_parser.add_argument('--tenant-id', help='Tenant ID (for Microsoft)')
    discovery_parser.add_argument('--instance-url', help='Instance URL (for Salesforce, e.g., login.salesforce.com)')
    discovery_parser.add_argument('--client-id', required=True, help='Client ID')
    discovery_parser.add_argument('--client-secret', help='Client Secret (optional)')
    discovery_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Authorization Code Flow
    auth_code_parser = subparsers.add_parser('auth-code', help='Authorization Code Flow')
    auth_code_parser.add_argument('--provider', required=True, choices=['microsoft', 'salesforce'], 
                                 help='OAuth provider')
    auth_code_parser.add_argument('--client-id', required=True, help='Client ID')
    auth_code_parser.add_argument('--client-secret', help='Client Secret (optional for PKCE)')
    auth_code_parser.add_argument('--tenant-id', help='Tenant ID (for Microsoft)')
    auth_code_parser.add_argument('--instance-url', help='Instance URL (for Salesforce)')
    auth_code_parser.add_argument('--scope', required=True, help='OAuth scopes (space-separated)')
    auth_code_parser.add_argument('--redirect-uri', default='http://localhost:8080/callback',
                                 help='Redirect URI')
    auth_code_parser.add_argument('--port', type=int, default=8080, help='Local server port')
    auth_code_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Client Credentials Flow
    client_creds_parser = subparsers.add_parser('client-credentials', help='Client Credentials Flow')
    client_creds_parser.add_argument('--provider', required=True, choices=['microsoft', 'salesforce'], 
                                    help='OAuth provider')
    client_creds_parser.add_argument('--client-id', required=True, help='Client ID')
    client_creds_parser.add_argument('--client-secret', required=True, help='Client Secret')
    client_creds_parser.add_argument('--tenant-id', help='Tenant ID (for Microsoft)')
    client_creds_parser.add_argument('--instance-url', help='Instance URL (for Salesforce)')
    client_creds_parser.add_argument('--scope', help='OAuth scopes (defaults to provider default)')
    client_creds_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'discover':
            return handle_discovery(args)
        elif args.command == 'auth-code':
            return handle_auth_code_flow(args)
        elif args.command == 'client-credentials':
            return handle_client_credentials_flow(args)
        else:
            print(f"Command '{args.command}' not implemented yet")
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def handle_discovery(args):
    """Handle OAuth discovery command"""
    if args.provider == 'microsoft':
        if not args.tenant_id:
            print("Error: --tenant-id is required for Microsoft provider")
            return 1
        
        analyze_client_capabilities(
            tenant_id=args.tenant_id,
            client_id=args.client_id,
            client_secret=args.client_secret,
            provider='microsoft',
            verbose=args.verbose
        )
        return 0
    elif args.provider == 'salesforce':
        analyze_client_capabilities(
            client_id=args.client_id,
            client_secret=args.client_secret,
            instance_url=args.instance_url,
            provider='salesforce',
            verbose=args.verbose
        )
        return 0
    else:
        print(f"Provider '{args.provider}' not supported for discovery")
        return 1


def handle_auth_code_flow(args):
    """Handle Authorization Code Flow"""
    
    # Initialize provider
    if args.provider == 'microsoft':
        if not args.tenant_id:
            print("Error: --tenant-id is required for Microsoft provider")
            return 1
        provider = MicrosoftOAuthProvider(args.tenant_id)
    elif args.provider == 'salesforce':
        provider = SalesforceOAuthProvider(args.instance_url)
    else:
        print(f"Provider '{args.provider}' not supported")
        return 1
    
    # Initialize flow
    flow = AuthorizationCodeFlow(
        provider=provider,
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=args.redirect_uri,
        scope=args.scope,
        verbose=args.verbose
    )
    
    # Execute the flow
    result = flow.execute(port=args.port)
    
    if result:
        print("\n✅ OAuth flow completed successfully!")
        return 0
    else:
        print("\n❌ OAuth flow failed")
        return 1


def handle_client_credentials_flow(args):
    """Handle Client Credentials Flow"""
    
    # Initialize provider
    if args.provider == 'microsoft':
        if not args.tenant_id:
            print("Error: --tenant-id is required for Microsoft provider")
            return 1
        provider = MicrosoftOAuthProvider(args.tenant_id)
    elif args.provider == 'salesforce':
        provider = SalesforceOAuthProvider(args.instance_url)
    else:
        print(f"Provider '{args.provider}' not supported")
        return 1
    
    # Use default scope if none provided
    scope = args.scope or provider.get_client_credentials_default_scope()
    
    if not args.scope:
        print(f"No scope provided, using default: {scope}")
        print("💡 Tip: Use --scope to specify custom scopes")
        print(f"   Recommended scopes: {', '.join(provider.get_recommended_client_credentials_scopes())}")
        print()
    
    # Initialize flow
    flow = ClientCredentialsFlow(
        provider=provider,
        client_id=args.client_id,
        client_secret=args.client_secret,
        #scope=scope,
        verbose=args.verbose
    )
    
    # Execute the flow
    result = flow.execute()
    
    if result:
        print("\n✅ OAuth flow completed successfully!")
        return 0
    else:
        print("\n❌ OAuth flow failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

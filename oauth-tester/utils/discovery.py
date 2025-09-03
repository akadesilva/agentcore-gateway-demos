"""
OAuth Discovery utilities to check provider capabilities
"""

import requests
import json


def discover_microsoft_capabilities(tenant_id, verbose=False):
    """
    Discover Microsoft OAuth capabilities for a tenant
    """
    discovery_url = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid_configuration"
    
    try:
        print(f"Fetching OAuth discovery information...")
        if verbose:
            print(f"Discovery URL: {discovery_url}")
        
        response = requests.get(discovery_url, timeout=10)
        response.raise_for_status()
        
        config = response.json()
        
        print("\n" + "="*60)
        print("OAUTH DISCOVERY INFORMATION")
        print("="*60)
        
        print(f"Issuer: {config.get('issuer', 'N/A')}")
        print(f"Authorization Endpoint: {config.get('authorization_endpoint', 'N/A')}")
        print(f"Token Endpoint: {config.get('token_endpoint', 'N/A')}")
        
        # Supported grant types
        grant_types = config.get('grant_types_supported', [])
        print(f"\nSupported Grant Types:")
        for grant in grant_types:
            print(f"  ✅ {grant}")
        
        # Supported response types
        response_types = config.get('response_types_supported', [])
        print(f"\nSupported Response Types:")
        for resp_type in response_types:
            print(f"  ✅ {resp_type}")
        
        # Supported scopes
        scopes = config.get('scopes_supported', [])
        if scopes:
            print(f"\nSupported Scopes:")
            for scope in scopes:
                print(f"  • {scope}")
        
        # Code challenge methods (PKCE)
        code_challenge_methods = config.get('code_challenge_methods_supported', [])
        if code_challenge_methods:
            print(f"\nSupported PKCE Methods:")
            for method in code_challenge_methods:
                print(f"  ✅ {method}")
        
        # Token endpoint auth methods
        token_auth_methods = config.get('token_endpoint_auth_methods_supported', [])
        if token_auth_methods:
            print(f"\nToken Endpoint Auth Methods:")
            for method in token_auth_methods:
                print(f"  ✅ {method}")
        
        if verbose:
            print(f"\nFull Discovery Response:")
            print("-" * 40)
            print(json.dumps(config, indent=2))
        
        return config
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch discovery information: {e}")
        return None


def discover_salesforce_capabilities(instance_url, verbose=False):
    """
    Discover Salesforce OAuth capabilities
    """
    if not instance_url.startswith('http'):
        instance_url = f"https://{instance_url}"
    
    discovery_url = f"{instance_url}/.well-known/openid-configuration"
    
    try:
        print(f"Fetching Salesforce OAuth discovery information...")
        if verbose:
            print(f"Discovery URL: {discovery_url}")
        
        response = requests.get(discovery_url, timeout=10)
        response.raise_for_status()
        
        config = response.json()
        
        print("\n" + "="*60)
        print("SALESFORCE OAUTH DISCOVERY INFORMATION")
        print("="*60)
        
        print(f"Issuer: {config.get('issuer', 'N/A')}")
        print(f"Authorization Endpoint: {config.get('authorization_endpoint', 'N/A')}")
        print(f"Token Endpoint: {config.get('token_endpoint', 'N/A')}")
        
        # Supported grant types
        grant_types = config.get('grant_types_supported', [])
        print(f"\nSupported Grant Types:")
        for grant in grant_types:
            print(f"  ✅ {grant}")
        
        # Supported response types
        response_types = config.get('response_types_supported', [])
        print(f"\nSupported Response Types:")
        for resp_type in response_types:
            print(f"  ✅ {resp_type}")
        
        # Supported scopes
        scopes = config.get('scopes_supported', [])
        if scopes:
            print(f"\nSupported Scopes:")
            for scope in scopes:
                print(f"  • {scope}")
        
        # Code challenge methods (PKCE)
        code_challenge_methods = config.get('code_challenge_methods_supported', [])
        if code_challenge_methods:
            print(f"\nSupported PKCE Methods:")
            for method in code_challenge_methods:
                print(f"  ✅ {method}")
        
        # Token endpoint auth methods
        token_auth_methods = config.get('token_endpoint_auth_methods_supported', [])
        if token_auth_methods:
            print(f"\nToken Endpoint Auth Methods:")
            for method in token_auth_methods:
                print(f"  ✅ {method}")
        
        if verbose:
            print(f"\nFull Discovery Response:")
            print("-" * 40)
            print(json.dumps(config, indent=2))
        
        return config
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch discovery information: {e}")
        print("Note: Salesforce discovery endpoint may not be available on all instances")
        return None


def test_microsoft_grant_types(tenant_id, client_id, client_secret=None, verbose=False):
    """
    Test which grant types are actually supported by making test requests
    """
    print("\n" + "="*60)
    print("TESTING GRANT TYPE SUPPORT")
    print("="*60)
    
    token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    # Test Client Credentials flow
    print("\n🔍 Testing Client Credentials Grant...")
    if client_secret:
        try:
            data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': 'https://graph.microsoft.com/.default'
            }
            
            response = requests.post(token_endpoint, data=data, timeout=10)
            
            if response.status_code == 200:
                print("  ✅ Client Credentials: SUPPORTED")
                if verbose:
                    token_info = response.json()
                    print(f"     Token type: {token_info.get('token_type', 'N/A')}")
                    print(f"     Expires in: {token_info.get('expires_in', 'N/A')} seconds")
            else:
                print(f"  ❌ Client Credentials: NOT SUPPORTED ({response.status_code})")
                if verbose:
                    try:
                        error = response.json()
                        print(f"     Error: {error.get('error', 'Unknown')}")
                        print(f"     Description: {error.get('error_description', 'N/A')}")
                    except:
                        print(f"     Response: {response.text}")
                        
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Client Credentials: ERROR - {e}")
    else:
        print("  ⚠️  Client Credentials: Cannot test (no client secret provided)")
    
    # Test Device Code flow
    print("\n🔍 Testing Device Code Grant...")
    device_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode"
    
    try:
        data = {
            'client_id': client_id,
            'scope': 'https://graph.microsoft.com/User.Read'
        }
        
        response = requests.post(device_endpoint, data=data, timeout=10)
        
        if response.status_code == 200:
            print("  ✅ Device Code: SUPPORTED")
            if verbose:
                device_info = response.json()
                print(f"     Device code: {device_info.get('device_code', 'N/A')[:20]}...")
                print(f"     User code: {device_info.get('user_code', 'N/A')}")
        else:
            print(f"  ❌ Device Code: NOT SUPPORTED ({response.status_code})")
            if verbose:
                try:
                    error = response.json()
                    print(f"     Error: {error.get('error', 'Unknown')}")
                except:
                    print(f"     Response: {response.text}")
                    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Device Code: ERROR - {e}")
    
    # Authorization Code flow requires user interaction, so we just indicate it's likely supported
    print("\n🔍 Authorization Code Grant:")
    print("  ✅ Authorization Code: LIKELY SUPPORTED (requires user interaction to test)")
    print("     Use the auth-code command to test this flow")


def test_salesforce_grant_types(instance_url, client_id, client_secret=None, verbose=False):
    """
    Test Salesforce grant types
    """
    if not instance_url.startswith('http'):
        instance_url = f"https://{instance_url}"
    
    print("\n" + "="*60)
    print("TESTING SALESFORCE GRANT TYPE SUPPORT")
    print("="*60)
    
    token_endpoint = f"{instance_url}/services/oauth2/token"
    
    # Test Client Credentials flow
    print("\n🔍 Testing Client Credentials Grant...")
    if client_secret:
        try:
            data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
            
            response = requests.post(token_endpoint, data=data, timeout=10)
            
            if response.status_code == 200:
                print("  ✅ Client Credentials: SUPPORTED")
                if verbose:
                    token_info = response.json()
                    print(f"     Token type: {token_info.get('token_type', 'N/A')}")
                    print(f"     Instance URL: {token_info.get('instance_url', 'N/A')}")
                    print(f"     Issued at: {token_info.get('issued_at', 'N/A')}")
            else:
                print(f"  ❌ Client Credentials: NOT SUPPORTED ({response.status_code})")
                if verbose:
                    try:
                        error = response.json()
                        print(f"     Error: {error.get('error', 'Unknown')}")
                        print(f"     Description: {error.get('error_description', 'N/A')}")
                    except:
                        print(f"     Response: {response.text}")
                        
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Client Credentials: ERROR - {e}")
    else:
        print("  ⚠️  Client Credentials: Cannot test (no client secret provided)")
    
    # Authorization Code flow requires user interaction
    print("\n🔍 Authorization Code Grant:")
    print("  ✅ Authorization Code: LIKELY SUPPORTED (requires user interaction to test)")
    print("     Use the auth-code command to test this flow")


def analyze_client_capabilities(tenant_id=None, client_id=None, client_secret=None, instance_url=None, provider='microsoft', verbose=False):
    """
    Comprehensive analysis of client capabilities
    """
    print("Analyzing OAuth client capabilities...")
    
    if provider == 'microsoft':
        print(f"Provider: Microsoft")
        print(f"Tenant ID: {tenant_id}")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {'Present' if client_secret else 'Not provided'}")
        
        # Get discovery information
        discovery_info = discover_microsoft_capabilities(tenant_id, verbose)
        
        # Test actual grant type support
        test_microsoft_grant_types(tenant_id, client_id, client_secret, verbose)
        
    elif provider == 'salesforce':
        instance_url = instance_url or 'login.salesforce.com'
        print(f"Provider: Salesforce")
        print(f"Instance URL: {instance_url}")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {'Present' if client_secret else 'Not provided'}")
        
        # Get discovery information
        discovery_info = discover_salesforce_capabilities(instance_url, verbose)
        
        # Test actual grant type support
        test_salesforce_grant_types(instance_url, client_id, client_secret, verbose)
    
    # Provide recommendations
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if client_secret:
        print("✅ You have a client secret, so you can use:")
        print("   • Client Credentials flow (for app-only access)")
        print("   • Authorization Code flow (for user access)")
        if provider == 'microsoft':
            print("   • Device Code flow (for devices without browsers)")
    else:
        print("⚠️  No client secret provided. You can use:")
        print("   • Authorization Code flow with PKCE (public client)")
        if provider == 'microsoft':
            print("   • Device Code flow (public client)")
        print("   • Cannot use Client Credentials flow")
    
    print("\n💡 Suggested testing order:")
    if client_secret:
        print("   1. Client Credentials (if you have a secret)")
    print("   2. Authorization Code with PKCE")
    if provider == 'microsoft':
        print("   3. Device Code flow")
    
    return discovery_info

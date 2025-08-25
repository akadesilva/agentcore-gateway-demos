"""
Client Credentials Flow implementation (2-Legged OAuth)
"""

import requests
import json
from utils.token_utils import display_token_info


class ClientCredentialsFlow:
    """Client Credentials Flow for app-to-app authentication"""
    
    def __init__(self, provider, client_id, client_secret, scope=None, verbose=False):
        self.provider = provider
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.verbose = verbose
        
        # Validate required parameters
        if not self.client_secret:
            raise ValueError("Client secret is required for Client Credentials flow")
        
        # Validate scope
        if self.scope:
            self.provider.validate_scope(self.scope)
    
    def request_token(self):
        """Request access token using client credentials"""
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        # Add scope if provided
        if self.scope:
            token_data['scope'] = self.scope
        
        # Add provider-specific parameters
        token_data.update(self.provider.get_additional_token_params())
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        if self.verbose:
            print(f"Token request to: {self.provider.token_endpoint}")
            print(f"Token data: {json.dumps({k: v for k, v in token_data.items() if k != 'client_secret'}, indent=2)}")
        
        try:
            response = requests.post(
                self.provider.token_endpoint,
                data=token_data,
                headers=headers,
                timeout=30
            )
            
            if self.verbose:
                print(f"Token response status: {response.status_code}")
                print(f"Token response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Token request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error response: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Error response: {e.response.text}")
            return None
    
    def execute(self):
        """Execute the Client Credentials Flow"""
        print(f"Starting Client Credentials Flow with {self.provider.name}")
        print(f"Client ID: {self.client_id}")
        print(f"Scope: {self.scope or 'Default scope'}")
        print()
        
        # Request token directly
        print("Requesting access token...")
        tokens = self.request_token()
        
        if not tokens:
            return False
        
        # Display token information
        print("\n" + "="*60)
        print("TOKEN RESPONSE")
        print("="*60)
        
        display_token_info(tokens, verbose=self.verbose)
        
        # Additional info for Client Credentials
        print(f"\n💡 Client Credentials Flow Notes:")
        print(f"   • This token represents your APPLICATION, not a user")
        print(f"   • Use this token to access resources your app has permission to")
        print(f"   • No refresh token provided (request new token when expired)")
        
        return True

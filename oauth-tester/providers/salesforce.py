"""
Salesforce OAuth Provider
"""

from .base import OAuthProvider


class SalesforceOAuthProvider(OAuthProvider):
    """Salesforce OAuth Provider"""
    
    def __init__(self, instance_url=None):
        # Default to login.salesforce.com for production, test.salesforce.com for sandbox
        self.instance_url = instance_url or "https://login.salesforce.com"
        if not self.instance_url.startswith('http'):
            self.instance_url = f"https://{self.instance_url}"
    
    @property
    def authorization_endpoint(self):
        return f"{self.instance_url}/services/oauth2/authorize"
    
    @property
    def token_endpoint(self):
        return f"{self.instance_url}/services/oauth2/token"
    
    @property
    def name(self):
        return "Salesforce"
    
    def get_default_scopes(self):
        """Return common Salesforce scopes"""
        return [
            "api",
            "refresh_token",
            "offline_access"
        ]
    
    def get_client_credentials_default_scope(self):
        """Return default scope for Client Credentials flow"""
        return "api"
    
    def validate_scope(self, scope):
        """Validate Salesforce-specific scope format"""
        scopes = scope.split()
        
        # Common Salesforce scopes
        valid_scopes = [
            "api", "web", "full", "chatter_api", "custom_permissions",
            "refresh_token", "offline_access", "openid", "profile", "email",
            "address", "phone", "id", "visualforce", "content", "wave_api",
            "eclair_api", "lightning", "cdp_ingest_api", "cdp_profile_api",
            "cdp_query_api", "cdp_segment_api", "pardot_api"
        ]
        
        for s in scopes:
            if s not in valid_scopes:
                print(f"Warning: Scope '{s}' may not be valid for Salesforce")
        
        return True
    
    def get_additional_auth_params(self):
        """Additional parameters for Salesforce authorization"""
        return {}
    
    def get_recommended_client_credentials_scopes(self):
        """Get recommended scopes for Client Credentials flow"""
        return [
            "api",
            "web", 
            "refresh_token"
        ]
    
    def get_recommended_auth_code_scopes(self):
        """Get recommended scopes for Authorization Code flow"""
        return [
            "api",
            "refresh_token", 
            "offline_access",
            "openid",
            "profile"
        ]

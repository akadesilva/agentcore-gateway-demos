"""
Microsoft OAuth Provider for Azure AD / Microsoft Graph
"""

from .base import OAuthProvider


class MicrosoftOAuthProvider(OAuthProvider):
    """Microsoft Azure AD OAuth Provider"""
    
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.base_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0"
    
    @property
    def authorization_endpoint(self):
        return f"{self.base_url}/authorize"
    
    @property
    def token_endpoint(self):
        return f"{self.base_url}/token"
    
    @property
    def name(self):
        return "Microsoft"
    
    def get_default_scopes(self):
        """Return common Microsoft Graph scopes"""
        return [
            "https://graph.microsoft.com/Sites.Read.All",
            "https://graph.microsoft.com/Files.ReadWrite.All",
            "offline_access"
        ]
    
    def get_client_credentials_default_scope(self):
        """Return default scope for Client Credentials flow"""
        return "https://graph.microsoft.com/.default"
    
    def validate_scope(self, scope):
        """Validate Microsoft-specific scope format"""
        scopes = scope.split()
        
        # Check for common Microsoft scope patterns
        valid_patterns = [
            "https://graph.microsoft.com/",
            "https://outlook.office.com/",
            "https://management.azure.com/",
            "openid",
            "profile", 
            "email",
            "offline_access"
        ]
        
        for s in scopes:
            if not any(s.startswith(pattern) or s == pattern for pattern in valid_patterns):
                print(f"Warning: Scope '{s}' may not be valid for Microsoft")
        
        # Special validation for Client Credentials
        if any(s.endswith('/.default') for s in scopes):
            print("ℹ️  Using .default scope - this requests all permissions granted to the app")
        
        return True
    
    def get_additional_auth_params(self):
        """Additional parameters for Microsoft authorization"""
        return {
            'response_mode': 'query'
        }
    
    def get_recommended_client_credentials_scopes(self):
        """Get recommended scopes for Client Credentials flow"""
        return [
            "https://graph.microsoft.com/.default",
            "https://graph.microsoft.com/Sites.Read.All",
            "https://graph.microsoft.com/Sites.ReadWrite.All",
            "https://graph.microsoft.com/Files.Read.All",
            "https://graph.microsoft.com/Files.ReadWrite.All"
        ]

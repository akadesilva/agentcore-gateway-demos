"""
Base OAuth Provider class
"""

from abc import ABC, abstractmethod


class OAuthProvider(ABC):
    """Abstract base class for OAuth providers"""
    
    @property
    @abstractmethod
    def authorization_endpoint(self):
        """Return the authorization endpoint URL"""
        pass
    
    @property
    @abstractmethod
    def token_endpoint(self):
        """Return the token endpoint URL"""
        pass
    
    @property
    @abstractmethod
    def name(self):
        """Return the provider name"""
        pass
    
    def get_default_scopes(self):
        """Return default scopes for this provider"""
        return []
    
    def validate_scope(self, scope):
        """Validate scope format for this provider"""
        return True
    
    def get_additional_auth_params(self):
        """Return additional parameters for authorization request"""
        return {}
    
    def get_additional_token_params(self):
        """Return additional parameters for token request"""
        return {}

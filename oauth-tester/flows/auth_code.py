"""
Authorization Code Flow implementation with PKCE support
"""

import base64
import hashlib
import secrets
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import requests
import json
from utils.token_utils import decode_jwt, display_token_info


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback"""
    
    def do_GET(self):
        """Handle GET request to callback endpoint"""
        # Parse the callback URL
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Store the authorization code or error
        if 'code' in query_params:
            self.server.auth_code = query_params['code'][0]
            self.server.state = query_params.get('state', [None])[0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html>
                <body>
                    <h2>Authorization Successful!</h2>
                    <p>You can close this window and return to the terminal.</p>
                    <script>setTimeout(function(){window.close();}, 3000);</script>
                </body>
                </html>
            ''')
        elif 'error' in query_params:
            self.server.auth_error = query_params['error'][0]
            self.server.error_description = query_params.get('error_description', [''])[0]
            
            # Send error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_msg = f"Error: {self.server.auth_error}"
            if self.server.error_description:
                error_msg += f" - {self.server.error_description}"
            
            self.wfile.write(f'''
                <html>
                <body>
                    <h2>Authorization Failed</h2>
                    <p>{error_msg}</p>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            '''.encode())
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


class AuthorizationCodeFlow:
    """Authorization Code Flow with PKCE support"""
    
    def __init__(self, provider, client_id, client_secret=None, redirect_uri=None, 
                 scope=None, verbose=False):
        self.provider = provider
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri or "http://localhost:8080/callback"
        self.scope = scope
        self.verbose = verbose
        
        # PKCE parameters
        self.code_verifier = None
        self.code_challenge = None
        self.state = None
        
        # Validate scope
        if self.scope:
            self.provider.validate_scope(self.scope)
    
    def generate_pkce_params(self):
        """Generate PKCE code verifier and challenge"""
        # Generate code verifier (43-128 characters)
        self.code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        
        # Generate code challenge
        challenge_bytes = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        self.code_challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')
        
        if self.verbose:
            print(f"Code Verifier: {self.code_verifier}")
            print(f"Code Challenge: {self.code_challenge}")
    
    def generate_state(self):
        """Generate state parameter for CSRF protection"""
        self.state = secrets.token_urlsafe(32)
        if self.verbose:
            print(f"State: {self.state}")
    
    def build_authorization_url(self):
        """Build the authorization URL"""
        self.generate_pkce_params()
        self.generate_state()
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'state': self.state,
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256'
        }
        
        # Add provider-specific parameters
        params.update(self.provider.get_additional_auth_params())
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        auth_url = f"{self.provider.authorization_endpoint}?{urllib.parse.urlencode(params)}"
        
        if self.verbose:
            print(f"Authorization URL: {auth_url}")
        
        return auth_url
    
    def start_callback_server(self, port):
        """Start local HTTP server to handle OAuth callback"""
        server = HTTPServer(('localhost', port), CallbackHandler)
        server.auth_code = None
        server.auth_error = None
        server.error_description = None
        server.state = None
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server
    
    def exchange_code_for_tokens(self, auth_code):
        """Exchange authorization code for tokens"""
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': self.code_verifier
        }
        
        # Add client secret if provided
        if self.client_secret:
            token_data['client_secret'] = self.client_secret
        
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
    
    def execute(self, port=8080):
        """Execute the Authorization Code Flow"""
        print(f"Starting Authorization Code Flow with {self.provider.name}")
        print(f"Client ID: {self.client_id}")
        print(f"Redirect URI: {self.redirect_uri}")
        print(f"Scope: {self.scope}")
        print()
        
        # Start callback server
        print(f"Starting callback server on port {port}...")
        server = self.start_callback_server(port)
        
        try:
            # Build authorization URL and open browser
            auth_url = self.build_authorization_url()
            print(f"Opening browser for authorization...")
            print(f"If browser doesn't open, visit: {auth_url}")
            print()
            
            webbrowser.open(auth_url)
            
            # Wait for callback
            print("Waiting for authorization callback...")
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while server.auth_code is None and server.auth_error is None:
                if time.time() - start_time > timeout:
                    print("Timeout waiting for authorization callback")
                    return False
                time.sleep(0.5)
            
            # Check for errors
            if server.auth_error:
                print(f"Authorization failed: {server.auth_error}")
                if server.error_description:
                    print(f"Description: {server.error_description}")
                return False
            
            # Verify state parameter
            if server.state != self.state:
                print("State parameter mismatch - possible CSRF attack")
                return False
            
            print("✅ Authorization code received")
            
            # Exchange code for tokens
            print("Exchanging authorization code for tokens...")
            tokens = self.exchange_code_for_tokens(server.auth_code)
            
            if not tokens:
                return False
            
            # Display token information
            print("\n" + "="*60)
            print("TOKEN RESPONSE")
            print("="*60)
            
            display_token_info(tokens, verbose=self.verbose)
            
            return True
            
        finally:
            server.shutdown()
            server.server_close()

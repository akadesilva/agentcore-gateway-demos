"""
Token utilities for JWT decoding and display
"""

import json
import base64
from datetime import datetime, timezone


def decode_jwt(token):
    """
    Decode JWT token without verification (for inspection only)
    Returns header and payload as dictionaries
    """
    try:
        # Split the token
        parts = token.split('.')
        if len(parts) != 3:
            return None, None
        
        # Decode header
        header_data = parts[0]
        # Add padding if needed
        header_data += '=' * (4 - len(header_data) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_data))
        
        # Decode payload
        payload_data = parts[1]
        # Add padding if needed
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        
        return header, payload
        
    except Exception as e:
        print(f"Failed to decode JWT: {e}")
        return None, None


def format_timestamp(timestamp):
    """Convert Unix timestamp to readable format"""
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return str(timestamp)


def display_jwt_info(token_name, token, verbose=False):
    """Display JWT token information"""
    print(f"\n{token_name}:")
    print("-" * 40)
    
    if verbose:
        print(f"Raw token: {token[:50]}...")
    
    header, payload = decode_jwt(token)
    
    if header and payload:
        print("✅ Valid JWT format")
        
        # Display key claims
        if 'sub' in payload:
            print(f"Subject (sub): {payload['sub']}")
        if 'aud' in payload:
            print(f"Audience (aud): {payload['aud']}")
        if 'iss' in payload:
            print(f"Issuer (iss): {payload['iss']}")
        if 'exp' in payload:
            exp_time = format_timestamp(payload['exp'])
            print(f"Expires (exp): {exp_time}")
        if 'iat' in payload:
            iat_time = format_timestamp(payload['iat'])
            print(f"Issued at (iat): {iat_time}")
        if 'scope' in payload:
            print(f"Scopes: {payload['scope']}")
        if 'scp' in payload:  # Microsoft uses 'scp' for scopes
            print(f"Scopes (scp): {' '.join(payload['scp'])}")
        
        # Microsoft-specific claims
        if 'cognito:username' in payload:
            print(f"Cognito Username: {payload['cognito:username']}")
        if 'cognito:groups' in payload:
            print(f"Cognito Groups: {', '.join(payload['cognito:groups'])}")
        if 'name' in payload:
            print(f"Name: {payload['name']}")
        if 'email' in payload:
            print(f"Email: {payload['email']}")
        if 'preferred_username' in payload:
            print(f"Username: {payload['preferred_username']}")
        if 'upn' in payload:  # Microsoft User Principal Name
            print(f"UPN: {payload['upn']}")
        
        if verbose:
            print(f"\nFull Header:")
            print(json.dumps(header, indent=2))
            print(f"\nFull Payload:")
            print(json.dumps(payload, indent=2))
    else:
        print("❌ Not a valid JWT or opaque token")
        if verbose:
            print(f"Token value: {token}")


def display_token_info(tokens, verbose=False):
    """Display information about all tokens in the response"""
    
    # Basic token info
    if 'access_token' in tokens:
        print(f"Access Token: Present ({'JWT' if is_jwt(tokens['access_token']) else 'Opaque'})")
    
    if 'id_token' in tokens:
        print(f"ID Token: Present (JWT)")
    
    if 'refresh_token' in tokens:
        print(f"Refresh Token: Present")
    
    if 'token_type' in tokens:
        print(f"Token Type: {tokens['token_type']}")
    
    if 'expires_in' in tokens:
        print(f"Expires In: {tokens['expires_in']} seconds")
    
    if 'scope' in tokens:
        print(f"Granted Scopes: {tokens['scope']}")
    
    # Display full token values for copying
    print(f"\n" + "="*60)
    print("FULL TOKEN VALUES (for copying)")
    print("="*60)
    
    if 'access_token' in tokens:
        print(f"\nAccess Token:")
        print("-" * 40)
        print(tokens['access_token'])
    
    if 'id_token' in tokens:
        print(f"\nID Token:")
        print("-" * 40)
        print(tokens['id_token'])
    
    if 'refresh_token' in tokens:
        print(f"\nRefresh Token:")
        print("-" * 40)
        print(tokens['refresh_token'])
    
    # Detailed token analysis
    if 'access_token' in tokens:
        if is_jwt(tokens['access_token']):
            display_jwt_info("Access Token (JWT)", tokens['access_token'], verbose)
        else:
            print(f"\nAccess Token Analysis (Opaque):")
            print("-" * 40)
            print("❌ Opaque token - cannot decode")
    
    if 'id_token' in tokens:
        display_jwt_info("ID Token Analysis", tokens['id_token'], verbose)
    
    if verbose:
        print(f"\nFull Token Response (JSON):")
        print("-" * 40)
        print(json.dumps(tokens, indent=2))


def is_jwt(token):
    """Check if a token is in JWT format"""
    try:
        parts = token.split('.')
        return len(parts) == 3
    except:
        return False

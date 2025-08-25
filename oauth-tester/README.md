# OAuth Tester

A CLI tool for testing various OAuth 2.0 flows with different providers.

## Features

- **OAuth Discovery**: Automatically detect supported grant types and capabilities
- **Authorization Code Flow** with PKCE support
- **Client Credentials Flow** for app-to-app authentication
- **Microsoft Azure AD / Graph** integration
- **JWT token decoding** and analysis
- Support for both **JWT and opaque access tokens**
- **Verbose debugging** output
- **Grant type testing** to verify what your client supports

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 🔍 Discover OAuth Capabilities (Recommended First Step)

Before testing OAuth flows, discover what your client supports:

```bash
# Basic discovery
python oauth_tester.py discover \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret

# Verbose discovery with full details
python oauth_tester.py discover \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --verbose
```

**What discovery shows you:**
- Supported grant types (authorization_code, client_credentials, device_code)
- Available scopes and endpoints
- PKCE support and authentication methods
- **Live testing** of Client Credentials and Device Code flows
- **Recommendations** for which flows to use

### 🤖 Client Credentials Flow (App-to-App)

For backend services and automated processes that don't involve users:

```bash
# Basic usage with default scope
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret

# With custom scope
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "https://graph.microsoft.com/Sites.Read.All"

# With verbose output
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "https://graph.microsoft.com/.default" \
  --verbose
```

**Client Credentials Notes:**
- No user interaction required
- Token represents your APPLICATION, not a user
- Requires client secret (confidential client)
- No refresh token provided (request new token when expired)
- Perfect for server-to-server scenarios

### 🔐 Authorization Code Flow (User Login)

```bash
# Basic usage
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --scope "https://graph.microsoft.com/Sites.Read.All offline_access"

# With verbose output
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --scope "https://graph.microsoft.com/Sites.Read.All offline_access" \
  --verbose

# Custom redirect URI and port
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --scope "https://graph.microsoft.com/Sites.Read.All" \
  --redirect-uri "http://localhost:3000/callback" \
  --port 3000

# With client secret (confidential client)
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "https://graph.microsoft.com/Sites.Read.All offline_access"
```

### Common Microsoft Graph Scopes

**For Client Credentials (.default recommended):**
- `https://graph.microsoft.com/.default` - All permissions granted to the app
- `https://graph.microsoft.com/Sites.Read.All` - Read SharePoint sites
- `https://graph.microsoft.com/Sites.ReadWrite.All` - Read/write SharePoint sites
- `https://graph.microsoft.com/Files.Read.All` - Read files
- `https://graph.microsoft.com/Files.ReadWrite.All` - Read/write files

**For Authorization Code (user context):**
- `https://graph.microsoft.com/Sites.Read.All` - Read SharePoint sites
- `https://graph.microsoft.com/Files.ReadWrite.All` - Read/write files
- `https://graph.microsoft.com/User.Read` - Read user profile
- `offline_access` - Get refresh tokens
- `openid profile email` - Get ID token with user info

## Azure App Registration Setup

### For Authorization Code Flow:
1. Go to Azure Portal > App Registrations
2. Create new registration or use existing
3. Add redirect URI: `http://localhost:8080/callback`
4. Note the Application (client) ID and Directory (tenant) ID
5. Configure API permissions for Microsoft Graph

### For Client Credentials Flow:
1. Same as above, but redirect URI not needed
2. **Create a client secret** in "Certificates & secrets"
3. **Grant admin consent** for application permissions
4. Use **Application permissions** (not Delegated permissions)

## Output

The tool will:
1. **Authorization Code**: Open browser, start callback server, exchange code for tokens
2. **Client Credentials**: Direct token request (no user interaction)
3. Display token information including:
   - Token types (JWT vs opaque)
   - Decoded JWT claims
   - Expiration times
   - Granted scopes

## Troubleshooting

- **Authorization Code**: Ensure redirect URI matches exactly in Azure app registration
- **Client Credentials**: Ensure admin consent is granted for application permissions
- Check that required scopes are granted in Azure
- Use `--verbose` flag for detailed debugging output
- Verify tenant ID and client ID are correct

### Common Microsoft Graph Scopes

- `https://graph.microsoft.com/Sites.Read.All` - Read SharePoint sites
- `https://graph.microsoft.com/Files.ReadWrite.All` - Read/write files
- `https://graph.microsoft.com/User.Read` - Read user profile
- `offline_access` - Get refresh tokens
- `openid profile email` - Get ID token with user info

## Azure App Registration Setup

1. Go to Azure Portal > App Registrations
2. Create new registration or use existing
3. Add redirect URI: `http://localhost:8080/callback`
4. Note the Application (client) ID and Directory (tenant) ID
5. Configure API permissions for Microsoft Graph

## Output

The tool will:
1. Open your browser for authorization
2. Start a local callback server
3. Exchange authorization code for tokens
4. Display token information including:
   - Token types (JWT vs opaque)
   - Decoded JWT claims
   - Expiration times
   - Granted scopes

## Troubleshooting

- Ensure redirect URI matches exactly in Azure app registration
- Check that required scopes are granted in Azure
- Use `--verbose` flag for detailed debugging output
- Verify tenant ID and client ID are correct

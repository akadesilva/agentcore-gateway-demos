# OAuth Tester

A CLI tool for testing various OAuth 2.0 flows with different providers.

## Features

- **OAuth Discovery**: Automatically detect supported grant types and capabilities
- **Authorization Code Flow** with PKCE support
- **Client Credentials Flow** for app-to-app authentication
- **Microsoft Azure AD / Graph** integration
- **Salesforce** OAuth integration
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
# Microsoft discovery
python oauth_tester.py discover \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret

# Salesforce discovery
python oauth_tester.py discover \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --instance-url login.salesforce.com

# Verbose discovery with full details
python oauth_tester.py discover \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --instance-url test.salesforce.com \
  --verbose
```

**What discovery shows you:**
- Supported grant types (authorization_code, client_credentials)
- Available scopes and endpoints (when supported by provider)
- PKCE support and authentication methods
- **Live testing** of Client Credentials flow
- **Recommendations** for which flows to use

### 🤖 Client Credentials Flow (App-to-App)

For backend services and automated processes that don't involve users:

#### Microsoft
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
```

#### Salesforce
```bash
# Basic usage with default scope
python oauth_tester.py client-credentials \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret

# With custom instance (sandbox)
python oauth_tester.py client-credentials \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --instance-url test.salesforce.com \
  --scope "api web"

# With verbose output
python oauth_tester.py client-credentials \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "api" \
  --verbose
```

### 👤 Authorization Code Flow (User Login)

For applications that need user authentication and consent:

#### Microsoft
```bash
# Basic user login flow
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --scope "https://graph.microsoft.com/Sites.Read.All offline_access"

# With custom redirect URI
python oauth_tester.py auth-code \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "https://graph.microsoft.com/User.Read" \
  --redirect-uri "http://localhost:3000/callback" \
  --port 3000
```

#### Salesforce
```bash
# Basic user login flow
python oauth_tester.py auth-code \
  --provider salesforce \
  --client-id your-client-id \
  --scope "api refresh_token"

# With sandbox instance
python oauth_tester.py auth-code \
  --provider salesforce \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --instance-url test.salesforce.com \
  --scope "api web refresh_token offline_access" \
  --redirect-uri "http://localhost:8080/callback"
```

## Provider-Specific Notes

### Microsoft Azure AD
- **Tenant ID required** for all operations
- Use `https://graph.microsoft.com/.default` for Client Credentials
- Application permissions require admin consent
- Access tokens are typically opaque (not JWT)
- **Discovery endpoint available** with full OpenID Connect support

### Salesforce
- **Instance URL** defaults to `login.salesforce.com` (production)
- Use `test.salesforce.com` for sandbox environments
- Common scopes: `api`, `web`, `refresh_token`, `offline_access`
- Access tokens are typically opaque
- **Discovery endpoint** may not be available on all instances

## Common Scopes

### Microsoft Graph
- `https://graph.microsoft.com/.default` - All granted permissions
- `https://graph.microsoft.com/Sites.Read.All` - Read SharePoint sites
- `https://graph.microsoft.com/User.Read` - Read user profile
- `offline_access` - Refresh token access

### Salesforce
- `api` - Access to APIs
- `web` - Web-based access
- `refresh_token` - Refresh token access
- `offline_access` - Offline access
- `openid profile email` - OpenID Connect scopes

## Troubleshooting

### Microsoft Issues
| Problem | Solution |
|---------|----------|
| "AADSTS70011: Invalid scope" | Use Microsoft Graph URLs, not SharePoint API |
| "AADSTS65001: No permission" | Grant admin consent in Azure portal |
| "AADSTS50194: Application not found" | Check Client ID and Tenant ID |

### Salesforce Issues
| Problem | Solution |
|---------|----------|
| "invalid_client_id" | Verify Connected App Client ID |
| "invalid_grant" | Check Client Secret and instance URL |
| "unsupported_grant_type" | Enable OAuth flows in Connected App |

### General OAuth Issues
| Problem | Solution |
|---------|----------|
| "Connection refused" | Check internet connection and firewall |
| "SSL certificate verify failed" | Update certificates or use --verbose |
| "Token expired" | Tokens are short-lived, get a new one |

## Examples

### Quick Microsoft Test
```bash
# Test if your Microsoft app works
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id abc123-def456 \
  --client-id xyz789 \
  --client-secret your-secret \
  --verbose
```

### Quick Salesforce Test
```bash
# Test if your Salesforce Connected App works
python oauth_tester.py client-credentials \
  --provider salesforce \
  --client-id your-consumer-key \
  --client-secret your-consumer-secret \
  --verbose
```

### Discovery Examples
```bash
# Discover Microsoft capabilities
python oauth_tester.py discover \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret

# Discover Salesforce capabilities
python oauth_tester.py discover \
  --provider salesforce \
  --client-id your-consumer-key \
  --client-secret your-consumer-secret \
  --instance-url login.salesforce.com
```

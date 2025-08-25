# OAuth 2.0 Flows Reference Guide

A comprehensive reference of OAuth 2.0 grant types and authentication flows.

## Standard OAuth 2.0 Flows

### 🔐 Authorization Code Flow
**Status**: ✅ **Recommended** (with PKCE)  
**Use Case**: Web applications, mobile apps, SPAs

**How it works:**
1. User clicks "Login" in your app
2. App redirects user to authorization server
3. User authenticates and grants permissions
4. Authorization server redirects back with authorization code
5. App exchanges code for tokens (server-side)

**Characteristics:**
- ✅ User login required
- ✅ Most secure flow
- ✅ Supports refresh tokens
- ✅ Client secret optional (with PKCE)
- ✅ Gets both access and ID tokens

**Best for:**
- Web applications with backend
- Single-page applications (with PKCE)
- Mobile applications (with PKCE)

---

### 🤖 Client Credentials Flow (2-Legged OAuth)
**Status**: ✅ **Active**  
**Use Case**: Server-to-server, backend services

**How it works:**
1. App sends client ID + client secret to token endpoint
2. Authorization server returns access token immediately
3. No user interaction required

**Characteristics:**
- ❌ No user involved
- ✅ Requires client secret
- ✅ Application identity (not user)
- ❌ No refresh token
- ✅ Simple and fast

**Best for:**
- Automated data processing
- Background services
- API-to-API communication
- Scheduled tasks

---

### 📱 Device Authorization Grant (Device Flow)
**Status**: ✅ **Active**  
**Use Case**: Devices without browsers or limited input

**How it works:**
1. Device requests device code from authorization server
2. Device displays user code and verification URL
3. User goes to another device (phone/computer) to authorize
4. Device polls token endpoint until user completes authorization
5. Device receives access token

**Characteristics:**
- ✅ User login required (on different device)
- ✅ No browser required on device
- ✅ Supports refresh tokens
- ✅ User identity
- ⏱️ Polling mechanism

**Best for:**
- Smart TVs
- IoT devices
- CLI tools on headless servers
- Gaming consoles

---

### 🔑 Resource Owner Password Credentials (ROPC)
**Status**: ⚠️ **Deprecated/Discouraged**  
**Use Case**: Legacy systems, trusted applications

**How it works:**
1. User enters username/password directly in your app
2. App sends credentials + client credentials to token endpoint
3. Authorization server returns tokens

**Characteristics:**
- ✅ User login required
- ⚠️ App sees user's password
- ❌ No MFA support
- ❌ Breaks SSO
- ✅ Simple for legacy migration

**Why deprecated:**
- Security risk if app is compromised
- No support for modern auth features
- Violates OAuth principle of not sharing passwords

---

### 🌐 Implicit Grant
**Status**: ❌ **Deprecated**  
**Use Case**: Single-page applications (legacy)

**How it works:**
1. User redirected to authorization server
2. User authenticates
3. Access token returned directly in URL fragment
4. JavaScript extracts token from URL

**Characteristics:**
- ✅ User login required
- ❌ No client secret
- ❌ Token exposed in URL
- ❌ No refresh token
- ⚠️ Security vulnerabilities

**Why deprecated:**
- Access token visible in browser history
- Vulnerable to token theft
- No way to authenticate client
- Replaced by Authorization Code + PKCE

---

## Non-OAuth Authentication Protocols

### 🔐 SRP (Secure Remote Password)
**Status**: ✅ **Active** (specific providers)  
**Use Case**: Secure password verification

**What it is:**
- Cryptographic protocol for password authentication
- Proves password knowledge without transmitting it
- **Not an OAuth flow** - used before OAuth

**Where used:**
- AWS Cognito User Pools
- Apple iCloud
- Some VPN clients

**Relationship to OAuth:**
```
SRP Authentication → OAuth Token Exchange
```

---

## Token Types Explained

### Access Token
- **Purpose**: Access protected resources
- **Format**: JWT or opaque (provider-dependent)
- **Audience**: Resource server/API
- **Contains**: Permissions, scopes, expiration

### ID Token
- **Purpose**: Identify the authenticated user
- **Format**: Always JWT
- **Audience**: Client application
- **Contains**: User identity claims (name, email, etc.)

### Refresh Token
- **Purpose**: Get new access tokens
- **Format**: Opaque string
- **Audience**: Authorization server
- **Contains**: Long-lived credential for token renewal

---

## Flow Selection Guide

### For Backend Services (No User)
✅ **Client Credentials Flow**
- Automated processing
- Server-to-server communication
- Application permissions

### For Web Applications (User Login)
✅ **Authorization Code Flow**
- Traditional web apps with backend
- Most secure option
- Supports all token types

### For Single-Page Apps (Browser Only)
✅ **Authorization Code + PKCE**
- Modern replacement for Implicit Grant
- No client secret needed
- Secure for public clients

### For Mobile Apps
✅ **Authorization Code + PKCE**
- Native mobile applications
- Secure without client secret
- Supports app-to-app redirects

### For Devices Without Browsers
✅ **Device Authorization Grant**
- Smart TVs, IoT devices
- CLI tools on servers
- Gaming consoles

### Legacy/Special Cases
⚠️ **ROPC** (if absolutely necessary)
- Only for highly trusted applications
- When other flows aren't feasible
- Plan migration to modern flows

---

## Security Best Practices

### Always Use:
- ✅ HTTPS for all communications
- ✅ State parameter (CSRF protection)
- ✅ PKCE for public clients
- ✅ Short-lived access tokens
- ✅ Secure token storage

### Never Do:
- ❌ Store tokens in localStorage (use httpOnly cookies)
- ❌ Log tokens in application logs
- ❌ Use Implicit Grant for new applications
- ❌ Hardcode client secrets in frontend code
- ❌ Use ROPC unless absolutely necessary

### Microsoft-Specific Notes:
- Use `.default` scope for Client Credentials
- Application permissions require admin consent
- Access tokens are typically opaque (not JWT)
- ID tokens are always JWT when using OpenID Connect scopes

---

## Quick Reference Commands

```bash
# Discovery (recommended first step)
python oauth_tester.py discover --provider microsoft --tenant-id <tenant> --client-id <id> --client-secret <secret>

# Client Credentials (app-only)
python oauth_tester.py client-credentials --provider microsoft --tenant-id <tenant> --client-id <id> --client-secret <secret>

# Authorization Code (user login)
python oauth_tester.py auth-code --provider microsoft --tenant-id <tenant> --client-id <id> --scope "https://graph.microsoft.com/Sites.Read.All"
```

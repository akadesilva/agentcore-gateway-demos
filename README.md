# AgentCore Gateway Demos

A collection of integration demos and tools for AWS Bedrock Agent Core Gateway, featuring OAuth 2.0 flows, SharePoint integration, and enterprise authentication patterns.

## 🎯 Project Overview

This repository demonstrates how to build secure, enterprise-grade integrations with AWS Bedrock Agent Core Gateway. The current focus is on OAuth 2.0 authentication flows and Microsoft SharePoint integration, providing a foundation for AI agents to access enterprise data securely.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Bedrock       │    │   AgentCore      │    │   OAuth 2.0     │    │   Microsoft      │
│   Agent         │◄──►│   Gateway        │◄──►│   Client        │◄──►│   Graph API      │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
                                                         │                        │
                                                         ▼                        ▼
                                               ┌─────────────────┐    ┌──────────────────┐
                                               │   OAuth Tester  │    │   SharePoint     │
                                               │   CLI Tool      │    │   Sites & Data   │
                                               └─────────────────┘    └──────────────────┘
```

## 🚀 What's Included

### 1. OAuth 2.0 Testing Toolkit (`oauth-tester/`)
A comprehensive CLI tool for testing and debugging OAuth 2.0 flows:

- **Multi-flow support**: Authorization Code, Client Credentials, Device Flow
- **Provider discovery**: Automatic capability detection
- **JWT token analysis**: Decode and inspect tokens
- **Microsoft Graph integration**: Specialized for SharePoint access
- **Verbose debugging**: Detailed error diagnostics

### 2. SharePoint API Client (`sharepoint/`)
A Python client for accessing SharePoint via Microsoft Graph:

- **Site enumeration**: List and search SharePoint sites
- **Token validation**: Test access token validity
- **Error handling**: Clear diagnostics for permission issues
- **Microsoft Graph integration**: Modern API approach

### 3. Documentation
- **OAuth Cheat Sheet**: Comprehensive guide to OAuth 2.0 flows
- **Setup guides**: Step-by-step configuration instructions
- **Troubleshooting**: Common issues and solutions

## 📁 Project Structure

```
agentcore-gateway-demos/
├── README.md                        # This file
├── oauth-cheatsheet.md             # Comprehensive OAuth 2.0 reference
├── oauth-tester/                   # OAuth 2.0 Testing Toolkit
│   ├── oauth_tester.py            # Main CLI application
│   ├── providers/
│   │   ├── microsoft.py           # Microsoft OAuth provider
│   │   └── base.py                # Base provider class
│   ├── flows/
│   │   ├── auth_code.py           # Authorization Code + PKCE
│   │   └── client_credentials.py  # Client Credentials flow
│   ├── utils/
│   │   ├── token_utils.py         # JWT decoding & display
│   │   └── discovery.py           # OAuth capability discovery
│   └── README.md
└── sharepoint/                     # SharePoint API Client
    ├── sharepoint_client.py       # SharePoint Graph API client
    └── README.md
```

## 🔧 Key Technical Achievements

### OAuth 2.0 Implementation
- **Client Credentials Flow**: Server-to-server authentication
- **PKCE Support**: Secure public client authentication
- **Token Analysis**: JWT decoding without verification
- **Error Handling**: Comprehensive diagnostics

### Microsoft Graph Integration
- **Application Permissions**: `Sites.Read.All` with admin consent
- **Tenant-specific endpoints**: Azure AD v2.0 endpoints
- **Scope management**: `.default` scope for application permissions
- **Token validation**: Proper audience and claims verification

### Enterprise Security
- **Admin consent workflow**: Proper permission delegation
- **Token expiration handling**: 1-hour token lifecycle
- **Secure credential management**: Client secret protection
- **Permission validation**: Role-based access control

## 🚀 Quick Start

### Prerequisites
- Azure tenant with admin access
- Python 3.8+
- AWS Bedrock Agent Core Gateway

### 1. Azure App Registration Setup
1. Create app registration in Azure Portal
2. Configure API permissions: **Microsoft Graph** > **Application** > **Sites.Read.All**
3. Grant admin consent
4. Create client secret
5. Note tenant ID, client ID, and client secret

### 2. Test OAuth Flow
```bash
cd oauth-tester
pip install -r requirements.txt

# Discover what your app supports
python oauth_tester.py discover \
  --provider microsoft \
  --tenant-id <your-tenant-id> \
  --client-id <your-client-id> \
  --client-secret <your-client-secret>

# Test Client Credentials flow
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id <your-tenant-id> \
  --client-id <your-client-id> \
  --client-secret <your-client-secret>
```

### 3. Access SharePoint
```bash
cd sharepoint

# Test your token
python sharepoint_client.py --token <access-token> --action test-token

# List SharePoint sites
python sharepoint_client.py --token <access-token> --action list-sites
```

### 4. Integrate with Bedrock Agent Core
- Configure OAuth client in AgentCore Identity
- Set up SharePoint MCP server
- Test with MCP Inspector

## 🎯 Use Cases Enabled

### Document Intelligence
- AI agents can read SharePoint documents
- Automated content analysis and summarization
- Intelligent document classification

### Knowledge Management
- AI-powered search across SharePoint sites
- Automated knowledge base updates
- Content recommendation systems

### Workflow Automation
- AI-driven approval processes
- Automated document routing
- Intelligent task assignment

## 🔍 Key Learnings & Troubleshooting

### Common OAuth Issues
1. **Microsoft Graph vs SharePoint API**: Must use Microsoft Graph permissions, not legacy SharePoint API permissions
2. **Application vs Delegated**: Client Credentials requires Application permissions with admin consent
3. **Scope specification**: Use `.default` scope for Client Credentials, not specific permission names
4. **Token propagation delay**: Admin consent changes can take 5-10 minutes to propagate

### Permission Verification
- Check `roles` field in JWT for application permissions
- Verify admin consent status in Azure Portal
- Use discovery tool to validate configuration

### Error Diagnostics
- 400/401/403 errors provide specific guidance
- Use `--verbose` flag for detailed debugging
- Token validation helps identify permission issues

## 🔮 Future Enhancements

### Planned Features
- **Device Flow implementation**: For headless server scenarios
- **Token refresh handling**: Automatic token renewal
- **Multi-tenant support**: Cross-organization access
- **Additional providers**: Google Drive, Dropbox integration
- **Batch operations**: Bulk SharePoint operations

### Potential Integrations
- **Meeting intelligence**: AI analysis of SharePoint-stored recordings
- **Compliance automation**: Automated document compliance checking
- **Content migration**: AI-assisted content organization
- **Security analysis**: Automated permission auditing

## 🤝 Contributing

This project demonstrates enterprise integration patterns and can be extended for:
- Additional OAuth providers
- Different Microsoft Graph APIs
- Alternative AI platforms
- Custom authentication flows

## 📚 References

- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [AWS Bedrock Agent Core](https://docs.aws.amazon.com/bedrock/)
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)

---

**Built with**: Python, OAuth 2.0, Microsoft Graph API, AWS Bedrock Agent Core

**Tags**: #OAuth2 #SharePoint #AWS #Bedrock #AI #Integration #Enterprise #Security

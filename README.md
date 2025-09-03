# AgentCore Gateway Demos

Connect AWS Bedrock Agent Core Gateway to enterprise services using OAuth 2.0. Get AI agents accessing your data in minutes.

## 🎯 What This Does

Enables secure integration between AWS Bedrock agents and enterprise services:
- **OAuth 2.0 authentication** with multiple providers
- **Enterprise data access** for AI agents via Agent Core Gateway
- **Complete testing toolkit** with debugging tools
- **Step-by-step setup guides** with visual instructions

## 🚀 Integration Guides

### Available Integrations

| Service | Status | Guide | Description |
|---------|--------|-------|-------------|
| **Microsoft SharePoint** | ✅ Ready | [SharePoint Quickstart](guides/sharepoint-quickstart.md) | Access SharePoint sites and documents |
| **Salesforce** | 🚧 Coming Soon | [Salesforce Integration](salesforce/README.md) | Connect to Salesforce CRM data |

### Getting Started

1. **Choose your integration** from the table above
2. **Follow the quickstart guide** for step-by-step setup
3. **Test with the included tools** to verify your configuration
4. **Connect to Agent Core Gateway** for AI agent access

## 🔧 Testing Tools

### OAuth Tester (`/oauth-tester/`)
Universal OAuth 2.0 testing toolkit:
- **Authorization Code Flow** with PKCE support
- **Client Credentials Flow** for app-to-app authentication
- **OAuth Discovery** to detect supported capabilities
- **JWT token analysis** and debugging

```bash
cd oauth-tester
pip install -r requirements.txt

# Test Microsoft OAuth
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id <tenant-id> \
  --client-id <client-id> \
  --client-secret <client-secret>
```

### Service-Specific Clients
Each integration includes a dedicated API client for testing:
- **SharePoint Client** (`/sharepoint/`) - Microsoft Graph API integration
- **Salesforce Client** (coming soon) - Salesforce REST API integration

## 📚 Documentation

- **[OAuth Flows Reference](oauth-cheatsheet.md)** - Complete OAuth 2.0 guide
- **[Integration Guides](guides/)** - Step-by-step setup instructions
- **Service READMEs** - Detailed documentation for each integration

## 🔧 Troubleshooting

### Common OAuth Issues
| Problem | Solution |
|---------|----------|
| "Permission denied" | Check API permissions in provider console |
| "Invalid scope" | Use provider-specific scope format |
| "Unauthorized" | Ensure admin consent is granted |
| "Token expired" | Check token expiration and refresh logic |

### Quick Diagnostics
- **Use verbose mode**: Add `--verbose` flag to all commands
- **Check token contents**: JWT tokens show permissions and expiration
- **Verify endpoints**: Use OAuth discovery to confirm configuration

## 📁 Repository Structure

```
├── guides/                 # Integration quickstart guides
├── oauth-tester/          # Universal OAuth 2.0 testing toolkit
├── sharepoint/           # SharePoint-specific tools and screenshots
├── salesforce/           # Salesforce integration (coming soon)
└── oauth-cheatsheet.md   # OAuth flows reference guide
```

## 🤝 Contributing

To add a new integration:

1. Create a new folder for your service (e.g., `/servicename/`)
2. Add a quickstart guide in `/guides/servicename-quickstart.md`
3. Include testing tools and API clients
4. Add screenshots for setup steps
5. Update this README with your integration

Each integration should follow the established pattern:
- OAuth provider setup
- Testing and validation tools
- Agent Core Gateway configuration
- End-to-end MCP testing

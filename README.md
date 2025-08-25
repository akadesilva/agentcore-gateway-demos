# AgentCore Gateway Demos

A collection of integration demos and tools for AWS Bedrock Agent Core Gateway, featuring OAuth 2.0 flows, SharePoint integration, and enterprise authentication patterns.

## 🎯 Project Overview

This repository demonstrates how to build secure, enterprise-grade integrations with AWS Bedrock Agent Core Gateway. The focus is on OAuth 2.0 flows with auth providers like Microsoft which are used to connect to commonly used data sources such as sharepoint, thus providing a foundation for AI agents to access enterprise data securely.

## 🏗️ Architecture for Microsoft services

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Bedrock       │    │   AgentCore      │    │   Microsoft     │    │   Microsoft      │
│   Agent         │◄──►│   Gateway        │◄──►│   Graph API     │◄──►│   Services       │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
                                           
```

## 🚀 What's Included

### 1. OAuth 2.0 Testing Toolkit (`oauth-tester/`)
A comprehensive CLI tool for testing and debugging OAuth 2.0 flows:

- **Multi-flow support**: Authorization Code, Client Credentials, Device Flow
- **Provider discovery**: Automatic capability detection
- **JWT token analysis**: Decode and inspect tokens
- **Microsoft Graph integration**: Specialized for testing integrations with Microsoft services
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
 


## 🚀 Quick Start for Microsoft Sharepoint

### Prerequisites
- Azure tenant with admin access
- Python 3.12+
- AWS Bedrock Agent Core Gateway

### 1. Azure App Registration Setup
1. Create app registration in Microsoft Entra Admin Center. Enter a friendly name and select 'Accounts in this organizational directory only' in 'Supported account types'

![Register app](register_app.png)

2. Configure API permissions: **Microsoft Graph** >  **Sites.Read.All**

![Grant permissions](add_permissions.png)

3. Note client ID, and client secret from step 1.

4. Note the tentant ID from the 'Home' section of the Microsoft Entra admin center

![Find tenant ID](find_tentant_id.png)


### 2. Test OAuth Flow for Microsoft (optional)
```bash
cd oauth-tester
pip install -r requirements.txt


# Test Client Credentials flow
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id <your-tenant-id> \
  --client-id <your-client-id> \
  --client-secret <your-client-secret>
```
Refer [README.md](oauth-tester/README.md) for more details


### 3. Test Sharepoint access (optional)
```bash
cd sharepoint

# Test your token
python sharepoint_client.py --token <access-token> --action test-token

# List SharePoint sites
python sharepoint_client.py --token <access-token> --action list-sites
```

Refer [README.md](sharepoint/README.md) for more details


### 4. Integrate with Bedrock Agent Core
- Configure OAuth client in AgentCore Identity as a OAuth client

![OAuth client](sharepoint/oauth_client_setup.png)

- Set up SharePoint as a target in Agent Core Gateway. Not sure how to create a Agent Core gateway? Refer [Creating your Gateway](!https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/create-gateway-methods.html)

![Add target for sharepoint](sharepoint/add_target_sharepoint.png)


### 5. Obtain Cognito access token for inbound auth
First we need to obtain an access token for inbound auth (i.e. authenticating the request from MCP INspector at the Agent Core Gateway) 

- In the Agent Core gateway console page, open the discovery URL and note the token endpoint. It would be in the below format:

```
    https://xxxxxxxxxxxx.auth.ap-southeast-2.amazoncognito.com/oauth2/token

```

- In the same discovery URL note the Cognito user pool ID that is being used to authenticate inbound requests by Agent Core Gateway.

![Find the user pool ID](find_user_pool_id.png)

- Navigate to Cognito and find the user pool with the same user pool id

![Navigate to Cognito user pool](find_user_pool.png)

- Note the client id and client secret from the 'App Clients' section of the user pool. This will be used to obtain the access token for inbound auth.

![Obtain client credentials](cognito_client_credentials.png)

- Run the below curl command to obtain the access token. This will be needed for the next step.

```

curl --http1.1 -X POST YOUR_TOKEN_ENDPOINT   -H "Content-Type: application/x-www-form-urlencoded"   -d "grant_type=client_credentials&client_id=YOUR_CLEINT_ID&client_secret=YOUR_CLIENT_SECRET"

```

### 6. Test in MCP inspector

- Install and start MCP inspector by running the command below:

```

npx @modelcontextprotocol/inspector

```

Refer [Using the MCP Inspector](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-using-inspector.html) for more information

Once the MCP server is running, it will open up a web page automatically. 

- Select Transport type as 'Streamable HTTP', URL as the Gateway resource URL in AgentCore gateway.
- Enter the access token obtained in previous step under 'Bearer Token'
- Click 'Connect'
- Click 'List Tools' and it should list sharepoint related tools like addSheet, getSite etc.

![MCP Inspector](mcp_inspector.png)

- Let us try to get site details. For this, you need to lookup the sharepoint siteId which is of the form <domain>,<guid>,<guid>
- Simply run the list-sites command to obtain the sharepoint site ID

```bash
cd sharepoint

# List SharePoint sites
python sharepoint_client.py --token <access-token> --action list-sites
```
- Run the tool and it will return the site information

![List sites](list_sites.png)






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




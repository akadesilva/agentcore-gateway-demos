# SharePoint API Client

A CLI tool for querying SharePoint sites using access tokens obtained from OAuth flows.

## Features

- **List SharePoint sites** with search capabilities
- **Get site details** for specific sites
- **Test access tokens** to verify permissions
- **Verbose debugging** output
- **Error handling** with clear messages

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Get Access Token

First, obtain an access token using the OAuth tester:

```bash
cd ../oauth-tester
python oauth_tester.py client-credentials \
  --provider microsoft \
  --tenant-id your-tenant-id \
  --client-id your-client-id \
  --client-secret your-client-secret \
  --scope "https://graph.microsoft.com/Sites.Read.All"
```

Copy the access token from the output.

### 2. Test Token

Verify your token works:

```bash
python sharepoint_client.py --token "your-access-token" --action test-token
```

### 3. List SharePoint Sites

```bash
# List all accessible sites
python sharepoint_client.py --token "your-access-token" --action list-sites

# Search for specific sites
python sharepoint_client.py --token "your-access-token" --action list-sites --search "project"

# Limit number of results
python sharepoint_client.py --token "your-access-token" --action list-sites --limit 10

# Verbose output
python sharepoint_client.py --token "your-access-token" --action list-sites --verbose
```

### 4. Get Site Details

```bash
python sharepoint_client.py --token "your-access-token" --action site-details --site-id "site-id-here"
```

## Required Permissions

Your Azure app registration needs these Microsoft Graph permissions:

**Application Permissions (for Client Credentials):**
- `Sites.Read.All` - Read all SharePoint sites
- `Sites.ReadWrite.All` - Read/write all SharePoint sites (if needed)

**Delegated Permissions (for Authorization Code):**
- `Sites.Read.All` - Read SharePoint sites user has access to
- `Sites.ReadWrite.All` - Read/write SharePoint sites user has access to

## Example Output

```
🔍 Querying SharePoint sites...
Listing all accessible sites

✅ Found 3 sites:
================================================================================

1. Project Alpha Site
   ID: contoso.sharepoint.com,12345678-1234-1234-1234-123456789012,abcdef12-3456-7890-abcd-ef1234567890
   URL: https://contoso.sharepoint.com/sites/project-alpha
   Description: Main project collaboration site
   Created: 2023-01-15 10:30:00 UTC
   Modified: 2024-08-20 14:22:33 UTC

2. HR Resources
   ID: contoso.sharepoint.com,87654321-4321-4321-4321-210987654321,fedcba09-8765-4321-dcba-098765432109
   URL: https://contoso.sharepoint.com/sites/hr-resources
   Description: Human Resources documentation and policies
   Created: 2023-03-22 09:15:00 UTC
   Modified: 2024-08-18 11:45:12 UTC
```

## Error Handling

The tool provides clear error messages for common issues:

- **401 Unauthorized**: Token expired or invalid
- **403 Forbidden**: Insufficient permissions
- **Network errors**: Connection issues

## Troubleshooting

1. **No sites found**: Check if your app has the required permissions
2. **401 errors**: Token may be expired, get a new one
3. **403 errors**: Ensure admin consent is granted for application permissions
4. **Use `--verbose`** flag for detailed debugging information

## Integration with OAuth Tester

This tool is designed to work with the OAuth tester in the parent directory:

1. Use OAuth tester to get access token
2. Copy the token from the output
3. Use this tool to query SharePoint with the token

Perfect for testing OAuth flows and verifying SharePoint access!

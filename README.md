# 🤖 Atlassian AI Assistant

**Talk to your Atlassian instance like ChatGPT.** Search and create Jira issues, Confluence pages, manage projects — all through natural language.

Built as an [Agent Zero](https://github.com/agent0ai/agent-zero) plugin. Uses the [Atlassian Cloud REST APIs](https://developer.atlassian.com/cloud/) to give AI agents full control over Jira and Confluence with a single Personal Access Token (PAT) per instance.

## 🚀 Want This Set Up for Your Business?

We're the team behind this plugin. We help companies automate their Atlassian workflows with AI.

**→ [Book a free discovery call](https://robulytics.com/contact)**  
**→ Email: oliver.mihatovic@robulytics.com**

What we offer:
- Custom setup & configuration for your Atlassian environments
- Integration with your specific Jira projects and Confluence spaces
- Employee training & AI adoption consulting
- Ongoing support & maintenance

---

## Features

- **Multi-instance support** – Connect to one or multiple Atlassian sites with isolated credentials
- **Jira & Confluence** – Full read and write operations for both products using a single API token
- **Credential isolation** – Each instance uses separate secrets and environment variables
- **Zero dependencies beyond Agent Zero** – Uses Python `requests` from the framework

## Installation

1. Copy this plugin to your Agent Zero installation:
   ```
   /a0/usr/plugins/atlassian/
   ```

2. Configure your Atlassian credentials as Agent Zero secrets and environment variables (see Configuration below).

3. Enable the plugin in Agent Zero settings (if not auto-enabled).

4. Verify the connection by asking Agent Zero:
   ```
   List my Confluence spaces
   ```

## Configuration

Each Atlassian instance requires:

| Variable | Type | Description |
|----------|------|-------------|
| `ATLASSIAN_BASEURL_<INSTANCE>` | Environment | Base URL (e.g. `https://your-domain.atlassian.net`) |
| `ATLASSIAN_PAT_<INSTANCE>` | Secret | Personal Access Token |
| `ATLASSIAN_EMAIL_<INSTANCE>` | Environment (optional) | Account email |

Example for a `YOUR_INSTANCE`:
- Secret: `ATLASSIAN_PAT_YOUR_INSTANCE` = your PAT
- Env vars:
  - `ATLASSIAN_BASEURL_YOUR_INSTANCE=https://your-domain.atlassian.net`
  - `ATLASSIAN_EMAIL_YOUR_INSTANCE=you@example.com`

Fallback: generic `ATLASSIAN_BASEURL`, `ATLASSIAN_PAT`, and `ATLASSIAN_EMAIL` are used when instance-specific values are missing.

## Usage Examples

```
# Confluence
"Show me the Confluence page with ID 12345 on my-instance"
"Search Confluence for pages about project plan on my-instance"
"List all Confluence spaces on my-instance"
"Create a new Confluence page titled 'Meeting Notes' in space ENG on my-instance"

# Jira
"Get details of Jira issue PROJ-1 on my-instance"
"Search Jira for all open issues in project PROJ"
"Create a new Jira task 'Update documentation' in project PROJ"
"Show me all Jira projects on my-instance"
```

## Tools

| Tool Name | Description |
|-----------|-------------|
| `atlassian` | Generic Atlassian tool supporting both Jira and Confluence with actions: `confluence_get_page`, `confluence_search`, `confluence_list_spaces`, `confluence_create_page`, `confluence_update_page`, `jira_get_issue`, `jira_search`, `jira_create_issue`, `jira_list_projects` |

## API Reference

This plugin uses the [Atlassian Cloud REST APIs](https://developer.atlassian.com/cloud/):

- **Confluence**: `/wiki/rest/api/` (v2)
- **Jira**: `/rest/api/3/` (v3)
- **Authentication**: Basic Auth (email:PAT base64 encoded)
- **Required Scopes**: Read & write access to Jira and Confluence

## Security

- API tokens stored as Agent Zero secrets (`ATLASSIAN_PAT_*`)
- No local data persistence beyond Atlassian API
- All requests use HTTPS
- Token never logged or exposed in responses

## Troubleshooting

### "Missing PAT for instance"
- Ensure the secret `ATLASSIAN_PAT_<INSTANCE>` (or generic `ATLASSIAN_PAT`) is configured in Agent Zero secrets

### "Connection failed" / 403 Forbidden
- Verify you're using Basic Auth (email:PAT base64), not Bearer token
- Check that the PAT is valid and has required scopes
- Ensure the base URL is correct and includes `https://`

### "Page not found"
- Verify the Confluence page ID (numeric, from URL or API)
- Check that the PAT user has permission to view the page

## Author

**Oliver Mihatovic** — AI Consultant & Founder at [Robulytics](https://www.robulytics.com)

> 💡 Want to automate your Atlassian workflows? [Book a free 15‑min call →](https://robulytics.com/contact)

## Disclaimer

This plugin is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall Robulytics be liable for any claim, damages, or other liability arising from the use of this software. Robulytics is an independent business and is not affiliated with, endorsed by, or sponsored by Atlassian or the Agent Zero project. All product names, logos, and brands are property of their respective owners.

## License

MIT License — free for personal and commercial use. See [LICENSE](LICENSE) file for details.

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

2. Configure your Atlassian credentials (see Configuration below).

3. Enable the plugin in Agent Zero settings (if not auto-enabled).

4. Verify the connection by asking Agent Zero:
   ```
   List my Confluence spaces
   ```

## Configuration

Each Atlassian instance requires three credentials. The plugin resolves them through a fallback chain:

### Base URL and Email (environment variables)

| Variable | Description |
|----------|-------------|
| `ATLASSIAN_BASEURL_<INSTANCE>` | Base URL, e.g. `https://your-domain.atlassian.net` |
| `ATLASSIAN_EMAIL_<INSTANCE>` | Account email for Basic Auth |

These must be set as **environment variables** in one of the following locations:

1. **`/a0/usr/.env`** (recommended) — the global env file loaded by Agent Zero at startup
2. **System environment variables** — set via Docker, shell, or other means

> ⚠️ **Note:** Project-level `variables.env` files (`.a0proj/variables.env`) are currently not loaded into the process environment by the Agent Zero framework. Place your Atlassian base URL and email in the global `/a0/usr/.env` file.

> ⚠️ **Important:** The base URL must include the protocol prefix (`https://`). Using just `your-domain.atlassian.net` without `https://` will cause a connection error.

Fallback: generic `ATLASSIAN_BASEURL` and `ATLASSIAN_EMAIL` (without instance suffix) are used when instance-specific values are missing.

### PAT / API Token (secrets)

| Variable | Description |
|----------|-------------|
| `ATLASSIAN_PAT_<INSTANCE>` | Personal Access Token |

The PAT is resolved through the following fallback chain:

1. **Environment variable** `ATLASSIAN_PAT_<INSTANCE>`
2. **Environment variable** `ATLASSIAN_PAT` (generic fallback)
3. **Agent Zero SecretsManager** lookup for `ATLASSIAN_PAT_<INSTANCE>` — loads from `usr/secrets.env` (global) and `.a0proj/secrets.env` (project-level)
4. **Agent Zero SecretsManager** lookup for `ATLASSIAN_PAT` (generic fallback)

The recommended approach is to store the PAT in Agent Zero's secrets manager (via `usr/secrets.env` or project-level `.a0proj/secrets.env`), which keeps it encrypted and out of plain-text environment files.

### Example Setup

For an instance called `ACME`:

**In `/a0/usr/.env`:**
```
ATLASSIAN_BASEURL_ACME="https://acme.atlassian.net"
ATLASSIAN_EMAIL_ACME="user@acme.com"
```

**In `/a0/usr/secrets.env` (or `.a0proj/secrets.env`):**
```
ATLASSIAN_PAT_ACME="your-personal-access-token"
```

Then use the plugin with `instance: "acme"`.

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
| `atlassian` | Generic Atlassian tool supporting both Jira and Confluence with actions: `confluence_get_page`, `confluence_search`, `confluence_list_spaces`, `confluence_create_page`, `confluence_update_page`, `confluence_get_page_children`, `confluence_list_pages`, `confluence_add_comment`, `confluence_get_comments`, `confluence_get_descendants`, `confluence_get_attachments`, `confluence_add_label`, `confluence_get_labels`, `jira_get_issue`, `jira_search`, `jira_create_issue`, `jira_list_projects`, `jira_update_issue`, `jira_add_comment`, `jira_get_comments`, `jira_transition_issue`, `jira_get_transitions`, `jira_assign_issue`, `jira_list_issues`, `jira_get_project`, `jira_list_issue_types`, `jira_list_priorities`, `jira_list_statuses`, `jira_list_users`, `jira_get_myself`, `jira_list_project_versions`, `jira_list_project_components`, `jira_get_fields`, `jira_get_issue_watchers`, `jira_add_watcher`, `jira_get_worklog`, `jira_add_worklog` |

## API Reference

This plugin uses the [Atlassian Cloud REST APIs](https://developer.atlassian.com/cloud/):

- **Confluence**: `/wiki/rest/api/` (v2)
- **Jira**: `/rest/api/3/` (v3)
- **Authentication**: Basic Auth (email:PAT base64 encoded)
- **Required Scopes**: Read & write access to Jira and Confluence

## Security

- API tokens resolved via Agent Zero SecretsManager (supports global and project-level secrets files)
- Environment variable fallback available for containerized deployments
- No local data persistence beyond Atlassian API
- All requests use HTTPS
- Token never logged or exposed in responses

## Troubleshooting

### "Missing base URL for instance"
- Ensure `ATLASSIAN_BASEURL_<INSTANCE>` is set in `/a0/usr/.env` (not only in project-level `variables.env`)
- The URL must include `https://` (e.g. `https://your-domain.atlassian.net`)
- Alternatively set the generic `ATLASSIAN_BASEURL` as a fallback

### "Missing PAT for instance"
- Ensure `ATLASSIAN_PAT_<INSTANCE>` is configured either as:
  - An environment variable, or
  - A secret in `usr/secrets.env` or `.a0proj/secrets.env`
- Alternatively set the generic `ATLASSIAN_PAT` as a fallback
- After adding secrets, restart Agent Zero for changes to take effect

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

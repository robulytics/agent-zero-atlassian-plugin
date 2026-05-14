# Atlassian Plugin Usage

This plugin provides the `atlassian` tool for Jira Cloud and Confluence Cloud.
A single Personal Access Token (PAT) works for both products on the same Atlassian domain.

## Instance Configuration

Each instance needs:
- **Base URL**: environment variable `ATLASSIAN_BASEURL_<INSTANCE>` (e.g. `ATLASSIAN_BASEURL_YOUR_INSTANCE=https://your-domain.atlassian.net`).
- **PAT**: stored as secret `ATLASSIAN_PAT_<INSTANCE>` (e.g. `ATLASSIAN_PAT_YOUR_INSTANCE`).
- **Email** (optional): `ATLASSIAN_EMAIL_<INSTANCE>` or `ATLASSIAN_EMAIL`.

Fallback: the tool also tries the generic `ATLASSIAN_BASEURL` and `ATLASSIAN_PAT` if instance-specific variables are absent.

## Tool Name
`atlassian`

## Required Arguments
- `instance` – e.g. `your-instance`
- `action` – one of the supported actions below

## Confluence Actions

### confluence_get_page
Fetch a Confluence page by ID.
- `page_id` (required, string)
- `expand` (optional, default `body.storage,version,space`)

### confluence_search
Search content with CQL.
- `cql` (required)
- `limit` (optional, default 10)

### confluence_list_spaces
List all spaces.
- `limit` (optional, default 50)

### confluence_create_page
Create a new page.
- `title` (required)
- `space_key` (required)
- `content` (storage-format HTML, required)
- `parent_id` (optional)

### confluence_update_page
Update an existing page.
- `page_id` (required)
- `title` (required)
- `space_key` (required)
- `content` (storage-format HTML, required)
- `version` (required, integer – increment from current)

## Jira Actions

### jira_get_issue
Get a Jira issue by key.
- `issue_key` (required, e.g. `PROJ-123`)
- `fields` (optional, e.g. `summary,status,assignee`)

### jira_search
Search issues with JQL.
- `jql` (required)
- `fields` (optional, default `summary,status,assignee,priority`)
- `max_results` (optional, default 10)

### jira_create_issue
Create a new issue.
- `summary` (required)
- `project_key` (required)
- `issuetype_name` (optional, default `Task`)
- `description` (optional, plain text)
- `priority_name` (optional)

### jira_list_projects
List all Jira projects. No extra arguments.

## Example Call
```json
{
  "tool_name": "atlassian",
  "tool_args": {
    "instance": "your-instance",
    "action": "jira_get_issue",
    "issue_key": "PROJ-1"
  }
}
```

## Authentication
Uses Basic Auth: `email:PAT` base64 encoded.

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

### confluence_get_page_children
Get direct children for a Confluence page.
- `page_id` (required)
- `expand` (optional, default `page`)
- `limit` (optional, default 25)

### confluence_list_pages
List Confluence pages (`type=page`).
- `space_key` (optional)
- `limit` (optional, default 25)
- `start` (optional, default 0)
- `expand` (optional)

### confluence_add_comment
Add a comment to a Confluence page.
- `page_id` (required)
- `body` (required)
- `representation` (optional, default `storage`)

### confluence_get_comments
Get comments for a Confluence page.
- `page_id` (required)
- `expand` (optional, default `body.storage,version`)
- `limit` (optional, default 25)

### confluence_get_descendants
Get descendants for a Confluence page.
- `page_id` (required)
- `expand` (optional, default `page`)
- `limit` (optional, default 25)

### confluence_get_attachments
Get attachments for a Confluence page.
- `page_id` (required)
- `expand` (optional)
- `limit` (optional, default 25)

### confluence_add_label
Add a global label to a Confluence page.
- `page_id` (required)
- `label` (required)

### confluence_get_labels
Get labels for a Confluence page.
- `page_id` (required)

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


## Additional Jira Actions
- jira_update_issue(issue_key, fields)
- jira_add_comment(issue_key, body)
- jira_get_comments(issue_key, max_results=10, start_at=0)
- jira_transition_issue(issue_key, transition_id, comment=None)
- jira_get_transitions(issue_key)
- jira_assign_issue(issue_key, account_id="")
- jira_list_issues(project_key, status=None, issuetype=None, max_results=20, fields="summary,status,assignee,priority")

# Tier 2 Jira Actions Specification

Add 9 new Jira actions to the Atlassian plugin.

## Files to Modify

1. `helpers/api.py` - Add client methods after existing Jira methods
2. `tools/atlassian.py` - Add dispatch actions before the `else` block

## Actions

### 1. jira_get_project
- API: GET /rest/api/3/project/{projectKey}
- api.py: `def jira_get_project(self, project_key: str) -> Dict:`
- No extra params
- atlassian.py args: project_key (required)

### 2. jira_list_issue_types
- API: GET /rest/api/3/issuetype
- api.py: `def jira_list_issue_types(self) -> Dict:`
- No params
- atlassian.py args: none required

### 3. jira_list_priorities
- API: GET /rest/api/3/priority
- api.py: `def jira_list_priorities(self) -> Dict:`
- No params
- atlassian.py args: none required

### 4. jira_list_statuses
- API: GET /rest/api/3/status
- api.py: `def jira_list_statuses(self) -> Dict:`
- No params
- atlassian.py args: none required

### 5. jira_list_users
- API: GET /rest/api/3/user/search
- api.py: `def jira_list_users(self, query: str = 
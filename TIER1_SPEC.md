# Tier 1 Jira Actions Specification

Add 7 new Jira actions to the Atlassian plugin.

## Files to Modify

1. `helpers/api.py` - Add client methods after line 144
2. `tools/atlassian.py` - Add dispatch actions before the `else` block at line 133

## Actions

### 1. jira_update_issue
- API: PUT /rest/api/3/issue/{issueKey}
- api.py: `def jira_update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict:`
- Payload: {"fields": fields}
- atlassian.py args: issue_key (required), fields (required, will be parsed from kwargs as JSON string or dict)

### 2. jira_add_comment
- API: POST /rest/api/3/issue/{issueKey}/comment
- api.py: `def jira_add_comment(self, issue_key: str, body: str) -> Dict:`
- Payload uses Atlassian Document Format: {"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": body}]}]}}
- atlassian.py args: issue_key (required), body (required)

### 3. jira_get_comments
- API: GET /rest/api/3/issue/{issueKey}/comment
- api.py: `def jira_get_comments(self, issue_key: str, max_results: int = 10, start_at: int = 0) -> Dict:`
- Params: {"maxResults": max_results, "startAt": start_at}
- atlassian.py args: issue_key (required), max_results (optional int default 10), start_at (optional int default 0)

### 4. jira_transition_issue
- API: POST /rest/api/3/issue/{issueKey}/transitions
- api.py: `def jira_transition_issue(self, issue_key: str, transition_id: str, comment: Optional[str] = None) -> Dict:`
- Base payload: {"transition": {"id": transition_id}}
- If comment, add: {"update": {"comment": [{"add": {"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment}]}]}}}]}}
- atlassian.py args: issue_key (required), transition_id (required), comment (optional)

### 5. jira_get_transitions
- API: GET /rest/api/3/issue/{issueKey}/transitions
- api.py: `def jira_get_transitions(self, issue_key: str) -> Dict:`
- No extra params
- atlassian.py args: issue_key (required)

### 6. jira_assign_issue
- API: PUT /rest/api/3/issue/{issueKey}/assignee
- api.py: `def jira_assign_issue(self, issue_key: str, account_id: str = "") -> Dict:`
- Payload: {"accountId": account_id}
- atlassian.py args: issue_key (required), account_id (optional, default empty)

### 7. jira_list_issues
- Wrapper around jira_search - build JQL dynamically
- api.py: `def jira_list_issues(self, project_key: str, status: Optional[str] = None, issuetype: Optional[str] = None, max_results: int = 20, fields: str = "summary,status,assignee,priority") -> Dict:`
- Build JQL: `f'project = {project_key}'`, append `AND status = "{status}"` and `AND issuetype = "{issuetype}"` if provided
- Call self.jira_search(jql, fields, max_results)
- atlassian.py args: project_key (required), status (optional), issuetype (optional), max_results (optional int default 20), fields (optional str)

## Also Update

- Description string in AtlassianTool class to include new action names
- Error message in the else block to list all supported actions
- Prompt file at prompts/atlassian.prompt.md to document new actions

## Testing

1. python -c "from helpers.api import AtlassianClient; print('api.py OK')"
2. python -c "from tools.atlassian import AtlassianTool; print('atlassian.py OK')"
3. Verify methods: python -c "from helpers.api import AtlassianClient; c = AtlassianClient('http://t','t','t'); print([m for m in dir(c) if m.startswith('jira_')])"
4. Grep for new action names in atlassian.py

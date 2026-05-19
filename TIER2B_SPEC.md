# Tier 2B: Watchers and Worklog Actions

Add 4 missing Jira actions. Files: helpers/api.py and tools/atlassian.py.

## Actions

### 1. jira_get_issue_watchers
- API: GET /rest/api/3/issue/{issueKey}/watchers
- api.py: def jira_get_issue_watchers(self, issue_key: str) -> Dict:
- No extra params
- atlassian.py: issue_key (required)

### 2. jira_add_watcher
- API: POST /rest/api/3/issue/{issueKey}/watchers
- api.py: def jira_add_watcher(self, issue_key: str, account_id: str) -> Dict:
- Payload: the account_id string as raw JSON string body
- Use self._request with json_data but pass account_id as the body
- NOTE: Jira expects the body to be a raw string (the accountId), not a JSON object. Use json=account_id approach. Actually the API expects: Content-Type: application/json with body being just the quoted string value like: "5b10ac8d82e05b22cc7d4ef5"
- For this, we need to POST with json_data set to just the string. But self._request passes json=dict. We need a workaround.
- SOLUTION: Add the account_id directly as the json payload. requests library json= will serialize a string as a JSON string.
- api.py implementation:
  def jira_add_watcher(self, issue_key: str, account_id: str) -> Dict:
      url = f"{self.base_url}/rest/api/3/issue/{issue_key}/watchers"
      resp = self.session.post(url, json=account_id)
      resp.raise_for_status()
      return resp.json() if resp.text else {}
- atlassian.py: issue_key (required), account_id (required)

### 3. jira_get_worklog
- API: GET /rest/api/3/issue/{issueKey}/worklog
- api.py: def jira_get_worklog(self, issue_key: str) -> Dict:
- No extra params
- atlassian.py: issue_key (required)

### 4. jira_add_worklog
- API: POST /rest/api/3/issue/{issueKey}/worklog
- api.py: def jira_add_worklog(self, issue_key: str, time_spent: str, comment: Optional[str] = None) -> Dict:
- Base payload: {"timeSpent": time_spent}
- If comment: {"timeSpent": time_spent, "comment": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment}]}]}}
- atlassian.py: issue_key (required), time_spent (required, e.g. "2h 30m"), comment (optional)

## Also Update
- Description string in AtlassianTool
- Error message in else block
- prompts/atlassian.prompt.md

## Testing
1. python -c "from helpers.api import AtlassianClient; print('OK')"
2. python -c "from helpers.api import AtlassianClient; c = AtlassianClient('http://t','t','t'); print(len([m for m in dir(c) if m.startswith('jira_')]))" — should be 24

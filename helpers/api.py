"""Unified Atlassian REST API client for Jira Cloud and Confluence Cloud."""
import requests
import base64
from typing import Optional, Dict, Any, List


class AtlassianClient:
    """
    Generic Atlassian Cloud client using Basic Auth (email:api_token).
    Works across Jira and Confluence from the same instance domain.
    """

    def __init__(self, base_url: str, email: str = "", api_token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        if email and api_token:
            credentials = f"{email}:{api_token}"
            encoded = base64.b64encode(credentials.encode()).decode()
            self.session.headers.update({
                "Authorization": f"Basic {encoded}",
                "Accept": "application/json",
            })

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        kwargs = {"params": params} if params else {}
        if json_data:
            kwargs["json"] = json_data
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.text else {}

    # ------------------------------------------------------------
    # Confluence API
    # ------------------------------------------------------------
    def confluence_get_page(self, page_id: str, expand: Optional[str] = None) -> Dict:
        params = {}
        if expand:
            params["expand"] = expand
        return self._request("GET", f"/wiki/rest/api/content/{page_id}", params=params)

    def confluence_search(self, cql: str, limit: int = 10) -> Dict:
        return self._request("GET", "/wiki/rest/api/content/search", params={"cql": cql, "limit": limit})

    def confluence_list_spaces(self, limit: int = 50) -> Dict:
        return self._request("GET", "/wiki/rest/api/space", params={"limit": limit})

    def confluence_create_page(
        self,
        title: str,
        space_key: str,
        content: str,
        parent_id: Optional[str] = None,
        representation: str = "storage",
    ) -> Dict:
        """
        Create a Confluence page.
        content: storage-format HTML
        representation: 'storage' (default) or 'wiki'
        """
        payload: Dict[str, Any] = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                representation: {"value": content, "representation": representation}
            },
        }
        if parent_id:
            payload["ancestors"] = [{"id": int(parent_id)}]
        return self._request("POST", "/wiki/rest/api/content", json_data=payload)

    def confluence_update_page(
        self,
        page_id: str,
        title: str,
        space_key: str,
        content: str,
        version: int,
        representation: str = "storage",
    ) -> Dict:
        payload = {
            "id": page_id,
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "version": {"number": version},
            "body": {
                representation: {"value": content, "representation": representation}
            },
        }
        return self._request("PUT", f"/wiki/rest/api/content/{page_id}", json_data=payload)


    def confluence_get_page_children(self, page_id: str, expand: str = "page", limit: int = 25) -> Dict:
        params = {"expand": expand, "limit": limit}
        return self._request("GET", f"/wiki/rest/api/content/{page_id}/child", params=params)

    def confluence_list_pages(
        self,
        space_key: Optional[str] = None,
        limit: int = 25,
        start: int = 0,
        expand: Optional[str] = None,
    ) -> Dict:
        params: Dict[str, Any] = {"type": "page", "limit": limit, "start": start}
        if space_key:
            params["spaceKey"] = space_key
        if expand:
            params["expand"] = expand
        return self._request("GET", "/wiki/rest/api/content", params=params)

    def confluence_add_comment(self, page_id: str, body: str, representation: str = "storage") -> Dict:
        payload: Dict[str, Any] = {
            "type": "comment",
            "container": {"id": page_id},
            "body": {
                representation: {"value": body, "representation": representation}
            },
        }
        return self._request("POST", "/wiki/rest/api/content", json_data=payload)

    def confluence_get_comments(self, page_id: str, expand: str = "body.storage,version", limit: int = 25) -> Dict:
        params = {"expand": expand, "limit": limit}
        return self._request("GET", f"/wiki/rest/api/content/{page_id}/child/comment", params=params)

    def confluence_get_descendants(self, page_id: str, expand: str = "page", limit: int = 25) -> Dict:
        params = {"expand": expand, "limit": limit}
        return self._request("GET", f"/wiki/rest/api/content/{page_id}/descendant", params=params)

    def confluence_get_attachments(self, page_id: str, expand: Optional[str] = None, limit: int = 25) -> Dict:
        params: Dict[str, Any] = {"limit": limit}
        if expand:
            params["expand"] = expand
        return self._request("GET", f"/wiki/rest/api/content/{page_id}/child/attachment", params=params)

    def confluence_add_label(self, page_id: str, label: str) -> Dict:
        payload = [{"prefix": "global", "name": label}]
        return self._request("POST", f"/wiki/rest/api/content/{page_id}/label", json_data=payload)

    def confluence_get_labels(self, page_id: str) -> Dict:
        return self._request("GET", f"/wiki/rest/api/content/{page_id}/label")

    # ------------------------------------------------------------
    # Jira API (v3)
    # ------------------------------------------------------------
    def jira_get_issue(self, issue_key: str, fields: Optional[str] = None) -> Dict:
        params = {}
        if fields:
            params["fields"] = fields
        return self._request("GET", f"/rest/api/3/issue/{issue_key}", params=params)

    def jira_search(self, jql: str, fields: Optional[str] = "summary,status,assignee,priority", max_results: int = 10) -> Dict:
        params = {"jql": jql, "fields": fields, "maxResults": max_results}
        return self._request("GET", "/rest/api/3/search", params=params)

    def jira_create_issue(
        self,
        summary: str,
        project_key: str,
        issuetype_name: str = "Task",
        description: str = "",
        priority_name: Optional[str] = None,
    ) -> Dict:
        payload = {
            "fields": {
                "summary": summary,
                "project": {"key": project_key},
                "issuetype": {"name": issuetype_name},
            }
        }
        if description:
            payload["fields"]["description"] = {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }]
            }
        if priority_name:
            payload["fields"]["priority"] = {"name": priority_name}
        return self._request("POST", "/rest/api/3/issue", json_data=payload)

    def jira_list_projects(self) -> Dict:
        return self._request("GET", "/rest/api/3/project")


    def jira_update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict:
        payload = {"fields": fields}
        return self._request("PUT", f"/rest/api/3/issue/{issue_key}", json_data=payload)

    def jira_add_comment(self, issue_key: str, body: str) -> Dict:
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": body}]
                }]
            }
        }
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/comment", json_data=payload)

    def jira_get_comments(self, issue_key: str, max_results: int = 10, start_at: int = 0) -> Dict:
        params = {"maxResults": max_results, "startAt": start_at}
        return self._request("GET", f"/rest/api/3/issue/{issue_key}/comment", params=params)

    def jira_transition_issue(self, issue_key: str, transition_id: str, comment: Optional[str] = None) -> Dict:
        payload: Dict[str, Any] = {"transition": {"id": transition_id}}
        if comment:
            payload["update"] = {
                "comment": [{
                    "add": {
                        "body": {
                            "type": "doc",
                            "version": 1,
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": comment}]
                            }]
                        }
                    }
                }]
            }
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/transitions", json_data=payload)

    def jira_get_transitions(self, issue_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/issue/{issue_key}/transitions")

    def jira_assign_issue(self, issue_key: str, account_id: str = "") -> Dict:
        payload = {"accountId": account_id}
        return self._request("PUT", f"/rest/api/3/issue/{issue_key}/assignee", json_data=payload)

    def jira_list_issues(
        self,
        project_key: str,
        status: Optional[str] = None,
        issuetype: Optional[str] = None,
        max_results: int = 20,
        fields: str = "summary,status,assignee,priority",
    ) -> Dict:
        jql = f"project = {project_key}"
        if status:
            jql += f' AND status = "{status}"'
        if issuetype:
            jql += f' AND issuetype = "{issuetype}"'
        return self.jira_search(jql, fields, max_results)


    def jira_get_project(self, project_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/project/{project_key}")

    def jira_list_issue_types(self) -> Dict:
        return self._request("GET", "/rest/api/3/issuetype")

    def jira_list_priorities(self) -> Dict:
        return self._request("GET", "/rest/api/3/priority")

    def jira_list_statuses(self) -> Dict:
        return self._request("GET", "/rest/api/3/status")

    def jira_list_users(self, query: str = "", max_results: int = 50, start_at: int = 0) -> Dict:
        params = {"query": query, "maxResults": max_results, "startAt": start_at}
        return self._request("GET", "/rest/api/3/user/search", params=params)

    def jira_get_myself(self) -> Dict:
        return self._request("GET", "/rest/api/3/myself")

    def jira_list_project_versions(self, project_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/project/{project_key}/versions")

    def jira_list_project_components(self, project_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/project/{project_key}/components")

    def jira_get_fields(self) -> Dict:
        return self._request("GET", "/rest/api/3/field")

    def jira_get_issue_watchers(self, issue_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/issue/{issue_key}/watchers")

    def jira_add_watcher(self, issue_key: str, account_id: str) -> Dict:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/watchers"
        resp = self.session.post(url, json=account_id)
        resp.raise_for_status()
        return resp.json() if resp.text else {}

    def jira_get_worklog(self, issue_key: str) -> Dict:
        return self._request("GET", f"/rest/api/3/issue/{issue_key}/worklog")

    def jira_add_worklog(self, issue_key: str, time_spent: str, comment: Optional[str] = None) -> Dict:
        payload: Dict[str, Any] = {"timeSpent": time_spent}
        if comment:
            payload["comment"] = {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment}]
                }]
            }
        return self._request("POST", f"/rest/api/3/issue/{issue_key}/worklog", json_data=payload)

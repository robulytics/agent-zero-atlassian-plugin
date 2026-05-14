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

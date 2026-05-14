import os
from typing import Optional, Dict, Any
from helpers.tool import Tool, Response
from usr.plugins.atlassian.helpers.api import AtlassianClient


class AtlassianTool(Tool):

    name = "atlassian"
    description = (
        "Generic Atlassian Cloud tool for Jira and Confluence. "
        "Use a single PAT (Personal Access Token) per instance. "
        "Actions: confluence_get_page, confluence_search, confluence_list_spaces, "
        "confluence_create_page, confluence_update_page, "
        "jira_get_issue, jira_search, jira_create_issue, jira_list_projects. "
        "Instance is selected via 'instance' argument."
    )

    async def execute(self, instance: str = "", action: str = "", **kwargs) -> Response:
        if not instance:
            return Response(message="Error: 'instance' argument is required (e.g., 'your-instance').", break_loop=False)
        if not action:
            return Response(message="Error: 'action' argument is required.", break_loop=False)

        # Build credentials from secrets and environment
        base_url_key = f"ATLASSIAN_BASEURL_{instance.upper()}"
        email_key = f"ATLASSIAN_EMAIL_{instance.upper()}"
        pat_secret = f"ATLASSIAN_PAT_{instance.upper()}"

        base_url = os.getenv(base_url_key) or os.getenv("ATLASSIAN_BASEURL")
        email = os.getenv(email_key) or os.getenv("ATLASSIAN_EMAIL", "")
        api_token = self.agent.get_secret(pat_secret) or self.agent.get_secret("ATLASSIAN_PAT")

        if not base_url:
            return Response(
                message=f"Missing base URL for instance '{instance}'. Set {base_url_key} or ATLASSIAN_BASEURL.",
                break_loop=False,
            )
        if not api_token:
            return Response(
                message=f"Missing PAT for instance '{instance}'. Add secret '{pat_secret}' or 'ATLASSIAN_PAT'.",
                break_loop=False,
            )

        client = AtlassianClient(base_url=base_url, email=email, api_token=api_token)

        try:
            result = await self._dispatch(client, action, **kwargs)
            return Response(message=str(result), break_loop=False)
        except Exception as e:
            return Response(message=f"Action '{action}' failed: {e}", break_loop=False)

    async def _dispatch(self, client: AtlassianClient, action: str, **kwargs) -> Dict[str, Any]:
        # Confluence actions
        if action == "confluence_get_page":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            expand = kwargs.get("expand", "body.storage,version,space")
            return client.confluence_get_page(page_id, expand)

        elif action == "confluence_search":
            cql = kwargs.get("cql")
            if not cql:
                raise ValueError("Missing 'cql' argument.")
            limit = kwargs.get("limit", 10)
            return client.confluence_search(cql, limit)

        elif action == "confluence_list_spaces":
            limit = kwargs.get("limit", 50)
            return client.confluence_list_spaces(limit)

        elif action == "confluence_create_page":
            title = kwargs.get("title")
            space_key = kwargs.get("space_key")
            content = kwargs.get("content", "")
            if not title or not space_key:
                raise ValueError("Missing 'title' or 'space_key'.")
            parent_id = kwargs.get("parent_id")
            representation = kwargs.get("representation", "storage")
            return client.confluence_create_page(
                title=title, space_key=space_key, content=content,
                parent_id=parent_id, representation=representation,
            )

        elif action == "confluence_update_page":
            page_id = kwargs.get("page_id")
            title = kwargs.get("title")
            space_key = kwargs.get("space_key")
            content = kwargs.get("content", "")
            version = kwargs.get("version")
            if not all([page_id, title, space_key, version]):
                raise ValueError("Missing required args for update (page_id, title, space_key, version).")
            representation = kwargs.get("representation", "storage")
            return client.confluence_update_page(
                page_id=page_id, title=title, space_key=space_key,
                content=content, version=int(version), representation=representation,
            )

        # Jira actions
        elif action == "jira_get_issue":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            fields = kwargs.get("fields")
            return client.jira_get_issue(issue_key, fields)

        elif action == "jira_search":
            jql = kwargs.get("jql")
            if not jql:
                raise ValueError("Missing 'jql' argument.")
            fields = kwargs.get("fields", "summary,status,assignee,priority")
            max_results = kwargs.get("max_results", 10)
            return client.jira_search(jql, fields, max_results)

        elif action == "jira_create_issue":
            summary = kwargs.get("summary")
            project_key = kwargs.get("project_key")
            if not summary or not project_key:
                raise ValueError("Missing 'summary' or 'project_key'.")
            issuetype_name = kwargs.get("issuetype_name", "Task")
            description = kwargs.get("description", "")
            priority_name = kwargs.get("priority_name")
            return client.jira_create_issue(
                summary=summary, project_key=project_key,
                issuetype_name=issuetype_name, description=description,
                priority_name=priority_name,
            )

        elif action == "jira_list_projects":
            return client.jira_list_projects()

        else:
            raise ValueError(f"Unknown action '{action}'. Supported: confluence_get_page, confluence_search, "
                             "confluence_list_spaces, confluence_create_page, confluence_update_page, "
                             "jira_get_issue, jira_search, jira_create_issue, jira_list_projects.")

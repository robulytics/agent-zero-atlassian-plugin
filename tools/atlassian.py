import os
from typing import Optional, Dict, Any
from helpers.tool import Tool, Response
from helpers.secrets import get_secrets_manager
from usr.plugins.atlassian.helpers.api import AtlassianClient


class AtlassianTool(Tool):

    name = "atlassian"
    description = (
        "Generic Atlassian Cloud tool for Jira and Confluence. "
        "Use a single PAT (Personal Access Token) per instance. "
        "Actions: confluence_get_page, confluence_search, confluence_list_spaces, "
        "confluence_create_page, confluence_update_page, confluence_get_page_children, "
        "confluence_list_pages, confluence_add_comment, confluence_get_comments, confluence_get_descendants, "
        "confluence_get_attachments, confluence_add_label, confluence_get_labels, "
        "jira_get_issue, jira_search, jira_create_issue, jira_list_projects, jira_update_issue, jira_add_comment, jira_get_comments, jira_transition_issue, jira_get_transitions, jira_assign_issue, jira_list_issues, jira_get_project, jira_list_issue_types, jira_list_priorities, jira_list_statuses, jira_list_users, jira_get_myself, jira_list_project_versions, jira_list_project_components, jira_get_fields, jira_get_issue_watchers, jira_add_watcher, jira_get_worklog, jira_add_worklog. "
        "Instance is selected via 'instance' argument."
    )

    def _resolve_secret(self, key: str) -> Optional[str]:
        """Resolve a secret via the framework's SecretsManager (global + project)."""
        try:
            sm = get_secrets_manager()
            secrets = sm.load_secrets()
            return secrets.get(key)
        except Exception:
            return None

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
        api_token = (
            os.getenv(pat_secret)
            or os.getenv("ATLASSIAN_PAT")
            or self._resolve_secret(pat_secret)
            or self._resolve_secret("ATLASSIAN_PAT")
        )

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

        elif action == "confluence_get_page_children":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            expand = kwargs.get("expand", "page")
            limit = int(kwargs.get("limit", 25))
            return client.confluence_get_page_children(page_id, expand, limit)

        elif action == "confluence_list_pages":
            space_key = kwargs.get("space_key")
            limit = int(kwargs.get("limit", 25))
            start = int(kwargs.get("start", 0))
            expand = kwargs.get("expand")
            return client.confluence_list_pages(space_key, limit, start, expand)

        elif action == "confluence_add_comment":
            page_id = kwargs.get("page_id")
            body = kwargs.get("body")
            if not page_id or not body:
                raise ValueError("Missing 'page_id' or 'body'.")
            representation = kwargs.get("representation", "storage")
            return client.confluence_add_comment(page_id, body, representation)

        elif action == "confluence_get_comments":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            expand = kwargs.get("expand", "body.storage,version")
            limit = int(kwargs.get("limit", 25))
            return client.confluence_get_comments(page_id, expand, limit)

        elif action == "confluence_get_descendants":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            expand = kwargs.get("expand", "page")
            limit = int(kwargs.get("limit", 25))
            return client.confluence_get_descendants(page_id, expand, limit)

        elif action == "confluence_get_attachments":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            expand = kwargs.get("expand")
            limit = int(kwargs.get("limit", 25))
            return client.confluence_get_attachments(page_id, expand, limit)

        elif action == "confluence_add_label":
            page_id = kwargs.get("page_id")
            label = kwargs.get("label")
            if not page_id or not label:
                raise ValueError("Missing 'page_id' or 'label'.")
            return client.confluence_add_label(page_id, label)

        elif action == "confluence_get_labels":
            page_id = kwargs.get("page_id")
            if not page_id:
                raise ValueError("Missing 'page_id' argument.")
            return client.confluence_get_labels(page_id)

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

        elif action == "jira_update_issue":
            issue_key = kwargs.get("issue_key")
            fields = kwargs.get("fields")
            if not issue_key or fields is None:
                raise ValueError("Missing 'issue_key' or 'fields'.")
            if isinstance(fields, str):
                import json
                fields = json.loads(fields)
            if not isinstance(fields, dict):
                raise ValueError("'fields' must be a dict or JSON object string.")
            return client.jira_update_issue(issue_key, fields)

        elif action == "jira_add_comment":
            issue_key = kwargs.get("issue_key")
            body = kwargs.get("body")
            if not issue_key or not body:
                raise ValueError("Missing 'issue_key' or 'body'.")
            return client.jira_add_comment(issue_key, body)

        elif action == "jira_get_comments":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            max_results = int(kwargs.get("max_results", 10))
            start_at = int(kwargs.get("start_at", 0))
            return client.jira_get_comments(issue_key, max_results, start_at)

        elif action == "jira_transition_issue":
            issue_key = kwargs.get("issue_key")
            transition_id = kwargs.get("transition_id")
            if not issue_key or not transition_id:
                raise ValueError("Missing 'issue_key' or 'transition_id'.")
            comment = kwargs.get("comment")
            return client.jira_transition_issue(issue_key, transition_id, comment)

        elif action == "jira_get_transitions":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            return client.jira_get_transitions(issue_key)

        elif action == "jira_assign_issue":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            account_id = kwargs.get("account_id", "")
            return client.jira_assign_issue(issue_key, account_id)

        elif action == "jira_list_issues":
            project_key = kwargs.get("project_key")
            if not project_key:
                raise ValueError("Missing 'project_key' argument.")
            status = kwargs.get("status")
            issuetype = kwargs.get("issuetype")
            max_results = int(kwargs.get("max_results", 20))
            fields = kwargs.get("fields", "summary,status,assignee,priority")
            return client.jira_list_issues(project_key, status, issuetype, max_results, fields)


        elif action == "jira_get_project":
            project_key = kwargs.get("project_key")
            if not project_key:
                raise ValueError("Missing 'project_key' argument.")
            return client.jira_get_project(project_key)

        elif action == "jira_list_issue_types":
            return client.jira_list_issue_types()

        elif action == "jira_list_priorities":
            return client.jira_list_priorities()

        elif action == "jira_list_statuses":
            return client.jira_list_statuses()

        elif action == "jira_list_users":
            query = kwargs.get("query", "")
            max_results = int(kwargs.get("max_results", 50))
            start_at = int(kwargs.get("start_at", 0))
            return client.jira_list_users(query, max_results, start_at)

        elif action == "jira_get_myself":
            return client.jira_get_myself()

        elif action == "jira_list_project_versions":
            project_key = kwargs.get("project_key")
            if not project_key:
                raise ValueError("Missing 'project_key' argument.")
            return client.jira_list_project_versions(project_key)

        elif action == "jira_list_project_components":
            project_key = kwargs.get("project_key")
            if not project_key:
                raise ValueError("Missing 'project_key' argument.")
            return client.jira_list_project_components(project_key)

        elif action == "jira_get_fields":
            return client.jira_get_fields()

        elif action == "jira_get_issue_watchers":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            return client.jira_get_issue_watchers(issue_key)

        elif action == "jira_add_watcher":
            issue_key = kwargs.get("issue_key")
            account_id = kwargs.get("account_id")
            if not issue_key or not account_id:
                raise ValueError("Missing 'issue_key' or 'account_id'.")
            return client.jira_add_watcher(issue_key, account_id)

        elif action == "jira_get_worklog":
            issue_key = kwargs.get("issue_key")
            if not issue_key:
                raise ValueError("Missing 'issue_key' argument.")
            return client.jira_get_worklog(issue_key)

        elif action == "jira_add_worklog":
            issue_key = kwargs.get("issue_key")
            time_spent = kwargs.get("time_spent")
            if not issue_key or not time_spent:
                raise ValueError("Missing 'issue_key' or 'time_spent'.")
            comment = kwargs.get("comment")
            return client.jira_add_worklog(issue_key, time_spent, comment)

        else:
            raise ValueError(f"Unknown action '{action}'. Supported: confluence_get_page, confluence_search, confluence_list_spaces, confluence_create_page, confluence_update_page, confluence_get_page_children, confluence_list_pages, confluence_add_comment, confluence_get_comments, confluence_get_descendants, confluence_get_attachments, confluence_add_label, confluence_get_labels, jira_get_issue, jira_search, jira_create_issue, jira_list_projects, jira_update_issue, jira_add_comment, jira_get_comments, jira_transition_issue, jira_get_transitions, jira_assign_issue, jira_list_issues, jira_get_project, jira_list_issue_types, jira_list_priorities, jira_list_statuses, jira_list_users, jira_get_myself, jira_list_project_versions, jira_list_project_components, jira_get_fields, jira_get_issue_watchers, jira_add_watcher, jira_get_worklog, jira_add_worklog.")

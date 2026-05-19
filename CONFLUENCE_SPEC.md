# Confluence Expansion Spec

Add 8 new Confluence actions. Files: helpers/api.py and tools/atlassian.py.
Total after: 13 Confluence actions (5 existing + 8 new).

## Actions

### 1. confluence_get_page_children
- API: GET /wiki/rest/api/content/{id}/child
- api.py: def confluence_get_page_children(self, page_id: str, expand: str = 'page', limit: int = 25) -> Dict:
- Params: expand, limit
- atlassian.py args: page_id (required), expand (optional default 'page'), limit (optional default 25)

### 2. confluence_list_pages
- API: GET /wiki/rest/api/content?type=page
- api.py: def confluence_list_pages(self, space_key: Optional[str] = None, limit: int = 25, start: int = 0, expand: Optional[str] = None) -> Dict:
- Params: always type=page, add spaceKey if space_key, limit, start, expand if provided
- atlassian.py args: space_key (optional), limit (optional default 25), start (optional default 0), expand (optional)

### 3. confluence_add_comment
- API: POST /wiki/rest/api/content
- api.py: def confluence_add_comment(self, page_id: str, body: str, representation: str = 'storage') -> Dict:
- Payload: type=comment, container has id=page_id, body uses storage format like existing confluence_create_page
- atlassian.py args: page_id (required), body (required), representation (optional default 'storage')

### 4. confluence_get_comments
- API: GET /wiki/rest/api/content/{id}/child/comment
- api.py: def confluence_get_comments(self, page_id: str, expand: str = 'body.storage,version', limit: int = 25) -> Dict:
- Params: expand, limit
- atlassian.py args: page_id (required), expand (optional default 'body.storage,version'), limit (optional default 25)

### 5. confluence_get_descendants
- API: GET /wiki/rest/api/content/{id}/descendant
- api.py: def confluence_get_descendants(self, page_id: str, expand: str = 'page', limit: int = 25) -> Dict:
- Params: expand, limit
- atlassian.py args: page_id (required), expand (optional default 'page'), limit (optional default 25)

### 6. confluence_get_attachments
- API: GET /wiki/rest/api/content/{id}/child/attachment
- api.py: def confluence_get_attachments(self, page_id: str, expand: Optional[str] = None, limit: int = 25) -> Dict:
- Params: expand, limit
- atlassian.py args: page_id (required), expand (optional), limit (optional default 25)

### 7. confluence_add_label
- API: POST /wiki/rest/api/content/{id}/label
- api.py: def confluence_add_label(self, page_id: str, label: str) -> Dict:
- Payload: list with one object: prefix=global, name=label
- atlassian.py args: page_id (required), label (required)

### 8. confluence_get_labels
- API: GET /wiki/rest/api/content/{id}/label
- api.py: def confluence_get_labels(self, page_id: str) -> Dict:
- No extra params
- atlassian.py args: page_id (required)

## Also Update
- Description string in AtlassianTool class
- Error message in else block
- prompts/atlassian.prompt.md

## Testing
1. python -c "from helpers.api import AtlassianClient; print('OK')"
2. python -c "from helpers.api import AtlassianClient; c = AtlassianClient('http://t','t','t'); m = [x for x in dir(c) if x.startswith('confluence_')]; print(m); print('Count:', len(m))" - should be 13
3. grep -c 'action == "confluence_' tools/atlassian.py - should be 13

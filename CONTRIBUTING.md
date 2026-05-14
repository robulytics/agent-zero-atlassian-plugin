# Contributing to Atlassian AI Assistant

Thanks for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs
- Search existing issues first to avoid duplicates
- Include: Atlassian plan (Free/Standard/Premium), Agent Zero version, Python version
- Share error messages and steps to reproduce

### Suggesting Features
- Open an issue with the `enhancement` label
- Describe the use case and why it matters for Atlassian users

### Pull Requests
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run existing tests if available
5. Submit a PR with a clear description

### Development Setup
```bash
git clone https://github.com/robulytics/agent-zero-atlassian-plugin
cd agent-zero-atlassian-plugin
# Place plugin files in /a0/usr/plugins/atlassian/
# Set ATLASSIAN_PAT secret and ATLASSIAN_BASEURL env var in Agent Zero
```

### Code Style
- Follow existing patterns in the plugin
- Use type hints where possible
- Add docstrings for new functions
- Keep tools focused on single Atlassian API operations
- Use the unified `AtlassianClient` helper for all API calls

## Getting Help

Questions? Reach out:
- Email: oliver.mihatovic@robulytics.com
- Website: https://robulytics.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

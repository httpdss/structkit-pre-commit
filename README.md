# structkit-pre-commit
pre-commit hook to validate StructKit YAML structures

## Usage

In your `.pre-commit-config.yaml`, reference this hook using a pinned release tag:

```yaml
repos:
  - repo: https://github.com/httpdss/structkit-pre-commit
    rev: v1.0.0  # Use the latest release tag
    hooks:
      - id: structkit-validate
```

**Note:** Always use a specific release tag (e.g., `v1.0.0`) for the `rev` field, not `main` or a branch name. This ensures reproducible pre-commit environments.

You can also use a floating major version tag (e.g., `rev: v1`) to automatically receive minor and patch updates, though full version tags are recommended for maximum reproducibility.

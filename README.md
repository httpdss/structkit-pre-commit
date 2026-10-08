# structkit-pre-commit

Companion to [StructKit](https://github.com/httpdss/structkit). Pre-commit hooks that validate `.structkit.yaml` before it lands (legacy `.struct.yaml` still matches). Star the [core repo](https://github.com/httpdss/structkit).

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- **structkit-validate**: Validates YAML syntax and StructKit schema compliance
- **structkit-lint**: Performs quality and safety checks on structure definitions

Both hooks run automatically on staged files matching the patterns:
- `.structkit.yaml` (default project file)
- `.struct.yaml` (legacy project file; still matched)
- `*.structkit.yaml` / `*.struct.yaml`
- `structures/**/*.yaml`
- `structures/**/*.yml`

## Installation

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/httpdss/structkit-pre-commit
    rev: v1.0.0  # Use the latest release
    hooks:
      - id: structkit-validate
      - id: structkit-lint
```

**Note:** Always use a specific release tag (e.g., `v1.0.0`) for the `rev` field, not `main` or a branch name. This ensures reproducible pre-commit environments.

You can also use a floating major version tag (e.g., `rev: v1`) to automatically receive minor and patch updates, though full version tags are recommended for maximum reproducibility.

Then install the hooks:

```bash
pre-commit install
```

## Hooks

### structkit-validate

Validates that StructKit YAML files are syntactically correct and conform to the StructKit schema.

**What it checks:**
- YAML syntax validity
- Top-level structure (must be a mapping)
- Required keys and value types
- File and folder configurations
- Variable declarations
- Hook definitions

**Example output on error:**

```
StructKit Validate...........................................................Failed
- hook id: structkit-validate
- exit code: 1

❗ Invalid YAML in .structkit.yaml: mapping values are not allowed here
```

### structkit-lint

Performs advanced quality and safety checks on StructKit structure definitions.

**What it checks:**
- Undefined template variables
- Unused declared variables
- Template syntax errors
- Duplicate entries (files, folders, variables)
- Unsafe hook commands (e.g., `rm -rf /`, piping to shell)
- Unpinned remote URLs
- Missing descriptions
- Naming conventions

**Example output:**

```
StructKit Lint...............................................................Passed
Linted 1 file(s): 0 error(s), 2 warning(s)
WARNING: .structkit.yaml: [missing-description] Missing top-level description.
WARNING: .structkit.yaml (files.README.md): [unpinned-remote-url] Remote URL is not pinned to a stable ref
```

## Hook Configuration

### Running only on specific files

You can customize which files the hooks run on:

```yaml
repos:
  - repo: https://github.com/httpdss/structkit-pre-commit
    rev: v1.0.0
    hooks:
      - id: structkit-validate
        files: ^structures/.*\.ya?ml$
      - id: structkit-lint
        files: \.(structkit|struct)\.ya?ml$
```

### Skip lint warnings

If you want to treat lint warnings as non-fatal:

```yaml
repos:
  - repo: https://github.com/httpdss/structkit-pre-commit
    rev: v1.0.0
    hooks:
      - id: structkit-validate
      - id: structkit-lint
        # Currently lint exits with code 1 on errors only
```

### Running hooks manually

You can run the hooks manually on specific files:

```bash
# Validate all structure files
pre-commit run structkit-validate --all-files

# Lint only staged files
pre-commit run structkit-lint

# Run on a specific file
pre-commit run structkit-validate --files .structkit.yaml
```

## CI/CD Integration

These hooks work seamlessly in CI environments. Add to your CI workflow:

```yaml
# GitHub Actions example
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
- name: Install pre-commit
  run: pip install pre-commit
- name: Run pre-commit hooks
  run: pre-commit run --all-files
```

## Requirements

- Python 3.8+
- [pre-commit](https://pre-commit.com/)
- [structkit](https://github.com/httpdss/structkit) (installed automatically)

## Manual Testing

To test the hooks without pre-commit:

```bash
# Install in development mode
pip install -e .

# Run validate hook
structkit-validate-hook .structkit.yaml

# Run lint hook (legacy .struct.yaml still works)
structkit-lint-hook .structkit.yaml .struct.yaml structures/*.yaml
```

## About StructKit

[StructKit](https://github.com/httpdss/structkit) is a YAML-based project scaffolding tool that helps you define and generate project structures from templates. It supports:

- Remote content from GitHub, S3, GCS, HTTP
- Template variables with Jinja2
- Pre/post generation hooks
- MCP integration for AI-assisted development

## Contributing

Contributions welcome! Please open an issue or pull request on [GitHub](https://github.com/httpdss/structkit-pre-commit).

## License

Apache-2.0 - see [LICENSE](LICENSE) for details.

## Links

- [StructKit Repository](https://github.com/httpdss/structkit)
- [StructKit Documentation](https://github.com/httpdss/structkit/tree/main/docs)
- [pre-commit Framework](https://pre-commit.com/)

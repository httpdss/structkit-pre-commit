"""Tests for pre-commit hook `files` patterns.

StructKit 3.3.0 renamed the default project file from `.struct.yaml` to
`.structkit.yaml`. Both names (and `*.struct.yaml` / `*.structkit.yaml`
structure files) must be matched.
"""
import re
from pathlib import Path

import pytest


HOOKS_FILE = Path(__file__).resolve().parent.parent / '.pre-commit-hooks.yaml'
FIXTURES_DIR = Path(__file__).resolve().parent / 'fixtures'

# Paths that must be selected by both hooks.
SHOULD_MATCH = [
    '.structkit.yaml',
    '.struct.yaml',
    '.structkit.yml',
    '.struct.yml',
    'foo/.structkit.yaml',
    'foo/.struct.yaml',
    'path/to/.structkit.yml',
    'valid.struct.yaml',
    'valid.structkit.yaml',
    'app.struct.yml',
    'app.structkit.yml',
    'structures/foo.yaml',
    'structures/bar.yml',
    'structures/nested/baz.yaml',
    'dir/structures/component.yml',
]

# Paths that must not be selected.
SHOULD_NOT_MATCH = [
    'README.md',
    'struct.yaml',
    'structkit.yaml',
    'mystruct.yaml',
    'config.yaml',
    'package.json',
    'tests/test_hooks.py',
    'src/structures.py',
    'foo.struct.json',
]


def _load_hook_files_patterns():
    """Return {hook_id: files_regex} from .pre-commit-hooks.yaml."""
    patterns = {}
    current_id = None
    for raw_line in HOOKS_FILE.read_text().splitlines():
        line = raw_line.strip()
        if line.startswith('id:'):
            current_id = line.split(':', 1)[1].strip()
        elif line.startswith('files:') and current_id:
            patterns[current_id] = line.split(':', 1)[1].strip()
    return patterns


class TestHookFilesPattern:
    """Verify both hooks match .structkit.yaml and legacy .struct.yaml."""

    @pytest.fixture(scope='class')
    def patterns(self):
        return _load_hook_files_patterns()

    def test_both_hooks_define_files(self, patterns):
        assert 'structkit-validate' in patterns
        assert 'structkit-lint' in patterns
        assert patterns['structkit-validate']
        assert patterns['structkit-lint']

    def test_hooks_share_the_same_files_pattern(self, patterns):
        assert patterns['structkit-validate'] == patterns['structkit-lint']

    @pytest.mark.parametrize('path', SHOULD_MATCH)
    def test_matches_structkit_and_legacy_paths(self, patterns, path):
        for hook_id, pattern in patterns.items():
            assert re.search(pattern, path), (
                f'{hook_id} pattern {pattern!r} should match {path!r}'
            )

    @pytest.mark.parametrize('path', SHOULD_NOT_MATCH)
    def test_does_not_match_unrelated_paths(self, patterns, path):
        for hook_id, pattern in patterns.items():
            assert not re.search(pattern, path), (
                f'{hook_id} pattern {pattern!r} should not match {path!r}'
            )

    def test_pattern_includes_structkit_and_legacy_struct(self, patterns):
        pattern = patterns['structkit-validate']
        assert 'structkit' in pattern
        assert 'struct' in pattern

    def test_fixture_filenames_match_pattern(self, patterns):
        pattern = patterns['structkit-validate']
        fixture_names = [
            path.name for path in FIXTURES_DIR.iterdir() if path.suffix in {'.yaml', '.yml'}
        ]
        assert any(name.endswith('.structkit.yaml') for name in fixture_names)
        assert any(name.endswith('.struct.yaml') for name in fixture_names)
        for name in fixture_names:
            assert re.search(pattern, name), f'fixture {name!r} should match {pattern!r}'

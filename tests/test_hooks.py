"""Tests for structkit pre-commit hooks."""
from pathlib import Path

import pytest

from structkit_validate_hook import main as validate_main
from structkit_lint_hook import main as lint_main


FIXTURES_DIR = Path(__file__).parent / 'fixtures'

# Cover both the StructKit 3.3.0 default name and the legacy filename.
STRUCTURE_SUFFIXES = ('.structkit.yaml', '.struct.yaml')


class TestValidateHook:
    """Tests for structkit-validate hook."""

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_valid_file(self, suffix):
        """Test that a valid file passes validation."""
        valid_file = str(FIXTURES_DIR / f'valid{suffix}')
        exit_code = validate_main([valid_file])
        assert exit_code == 0

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_invalid_yaml(self, suffix):
        """Test that invalid YAML fails validation."""
        invalid_file = str(FIXTURES_DIR / f'invalid_yaml{suffix}')
        exit_code = validate_main([invalid_file])
        assert exit_code == 1

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_invalid_schema(self, suffix):
        """Test that invalid schema fails validation."""
        invalid_file = str(FIXTURES_DIR / f'invalid_schema{suffix}')
        exit_code = validate_main([invalid_file])
        assert exit_code == 1

    def test_nonexistent_file(self):
        """Test that nonexistent file fails validation."""
        exit_code = validate_main(['nonexistent.yaml'])
        assert exit_code == 1

    def test_no_files(self):
        """Test that no files returns success."""
        exit_code = validate_main([])
        assert exit_code == 0

    def test_multiple_files(self):
        """Test validation of multiple files across both filenames."""
        valid_file = str(FIXTURES_DIR / 'valid.structkit.yaml')
        invalid_file = str(FIXTURES_DIR / 'invalid_yaml.struct.yaml')
        exit_code = validate_main([valid_file, invalid_file])
        assert exit_code == 1


class TestLintHook:
    """Tests for structkit-lint hook."""

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_valid_file(self, suffix):
        """Test that a valid file passes linting."""
        valid_file = str(FIXTURES_DIR / f'valid{suffix}')
        exit_code = lint_main([valid_file])
        assert exit_code == 0

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_file_with_warnings(self, suffix):
        """Test that warnings are reported but don't fail the hook."""
        warnings_file = str(FIXTURES_DIR / f'lint_warnings{suffix}')
        exit_code = lint_main([warnings_file])
        assert exit_code == 0

    @pytest.mark.parametrize('suffix', STRUCTURE_SUFFIXES)
    def test_invalid_yaml(self, suffix):
        """Test that invalid YAML fails linting."""
        invalid_file = str(FIXTURES_DIR / f'invalid_yaml{suffix}')
        exit_code = lint_main([invalid_file])
        assert exit_code == 1

    def test_nonexistent_file(self):
        """Test that nonexistent file fails linting."""
        exit_code = lint_main(['nonexistent.yaml'])
        assert exit_code == 1

    def test_no_files(self):
        """Test that no files returns success."""
        exit_code = lint_main([])
        assert exit_code == 0

    def test_multiple_files(self):
        """Test linting of multiple files across both filenames."""
        valid_file = str(FIXTURES_DIR / 'valid.structkit.yaml')
        warnings_file = str(FIXTURES_DIR / 'lint_warnings.struct.yaml')
        exit_code = lint_main([valid_file, warnings_file])
        assert exit_code == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

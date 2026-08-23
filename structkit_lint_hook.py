#!/usr/bin/env python3
"""Pre-commit hook wrapper for structkit lint."""
import subprocess
import sys
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        return 0

    result = subprocess.run(
        ['structkit', 'lint'] + list(argv),
        capture_output=False,
    )

    return result.returncode


if __name__ == '__main__':
    sys.exit(main())

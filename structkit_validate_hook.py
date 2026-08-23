#!/usr/bin/env python3
"""Pre-commit hook wrapper for structkit validate."""
import subprocess
import sys
from typing import List, Sequence


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        return 0

    exit_code = 0
    for filename in argv:
        result = subprocess.run(
            ['structkit', 'validate', filename],
            capture_output=False,
        )
        if result.returncode != 0:
            exit_code = 1

    return exit_code


if __name__ == '__main__':
    sys.exit(main())

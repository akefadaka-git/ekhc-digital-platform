#!/usr/bin/env python
"""Django management entry point for the EKHC OS foundation."""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - installation guidance
        raise ImportError(
            "Django is not installed. Install the pinned requirements first."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

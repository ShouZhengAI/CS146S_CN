#!/usr/bin/env python3
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskboard_project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

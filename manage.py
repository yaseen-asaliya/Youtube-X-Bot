#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_x_bot.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

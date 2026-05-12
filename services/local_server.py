"""
Local development entry point.
Runs the Lambda pipeline once, then starts Django for approval webhook testing.

Usage:
    python -m services.local_server                    # trigger + start server
    python -m services.local_server --only-server      # skip trigger, just serve
"""
import os
import sys
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_x_bot.settings")
django.setup()


def run_pipeline():
    from services.handler import lambda_handler
    result = lambda_handler({}, None)
    print(result)


def run_server(port: int = 8000):
    from django.core.management import call_command
    print(f"\nStarting approval server on http://localhost:{port}")
    call_command("runserver", f"0.0.0.0:{port}")


if __name__ == "__main__":
    only_server = "--only-server" in sys.argv
    if not only_server:
        run_pipeline()
    run_server()

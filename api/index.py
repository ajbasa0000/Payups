from payups.wsgi import app
from django.core.management import call_command
import sys

try:
    print("Running database migrations on startup...", file=sys.stderr)
    call_command('migrate', interactive=False)
    print("Database migrations applied successfully.", file=sys.stderr)
except Exception as e:
    print(f"Error running database migrations: {e}", file=sys.stderr)


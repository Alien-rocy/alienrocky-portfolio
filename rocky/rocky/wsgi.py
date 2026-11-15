"""WSGI entry point (used by Vercel and any WSGI server)."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rocky.settings")

application = get_wsgi_application()
app = application  # Vercel looks for `app` or `application`

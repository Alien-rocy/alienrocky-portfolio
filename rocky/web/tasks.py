import logging

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail

from .models import Project, Subscription

logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    """Email the latest projects to every subscriber.

    Run it with:  python manage.py send_newsletter
    (Celery was removed: Vercel can't run background workers.)
    """
    projects = Project.objects.order_by("-id")[:3]
    content = "\n".join(f"{p.title}: {p.description or ''}" for p in projects)
    sent = 0
    for sub in Subscription.objects.all():
        try:
            send_mail(
                subject="Alien_R Weekly Updates",
                message=(
                    f"Here are the latest projects:\n\n{content}\n\n"
                    f"Unsubscribe: {settings.SITE_URL}/unsubscribe/{signing.dumps(sub.email, salt='unsubscribe')}/"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.email],
            )
            sent += 1
        except Exception:
            logger.exception("Newsletter to %s failed", sub.email)
    return sent

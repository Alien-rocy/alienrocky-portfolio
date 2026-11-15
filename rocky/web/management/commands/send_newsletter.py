from django.core.management.base import BaseCommand

from web.tasks import send_weekly_newsletter


class Command(BaseCommand):
    help = "Send the weekly newsletter to all subscribers."

    def handle(self, *args, **options):
        self.stdout.write(f"Sent {send_weekly_newsletter()} email(s).")

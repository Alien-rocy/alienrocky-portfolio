from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Project, Subscription


class PublicPageTests(TestCase):
    def test_home_renders_featured_projects_and_links_to_detail(self):
        p = Project.objects.create(title="Demo", featured=True, status="Live", tech_stack="Python, Django")
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Demo")
        self.assertContains(resp, reverse("project_detail", args=[p.pk]))

    def test_project_detail_and_archive(self):
        p = Project.objects.create(title="Demo")
        self.assertEqual(self.client.get(reverse("project_detail", args=[p.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("Projects")).status_code, 200)

    def test_contact_validation_and_saving(self):
        bad = self.client.post(reverse("contact"), {"name": "A", "email": "nope", "message": "hi"})
        self.assertEqual(bad.status_code, 400)
        ok = self.client.post(reverse("contact"), {"name": "Ada", "email": "ada@example.com", "message": "Hello there"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_subscribe_and_signed_unsubscribe(self):
        self.client.post(reverse("subscribe"), {"email": "reader@example.com"})
        self.assertTrue(Subscription.objects.filter(email="reader@example.com").exists())
        # a plain email in the URL must NOT unsubscribe anyone
        self.client.get("/unsubscribe/reader@example.com/")
        self.assertTrue(Subscription.objects.filter(email="reader@example.com").exists())
        token = signing.dumps("reader@example.com", salt="unsubscribe")
        self.client.get(f"/unsubscribe/{token}/")
        self.assertFalse(Subscription.objects.filter(email="reader@example.com").exists())


class DashboardTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user("owner", password="pw12345!x")

    def login(self):
        self.assertTrue(self.client.login(username="owner", password="pw12345!x"))

    def test_dashboard_pages_require_login(self):
        for name in ("dashboard_home", "dashboard_projects_view", "add_project", "messages", "subscriptions", "testimonials"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 302, name)

    def test_dashboard_pages_render_when_logged_in(self):
        self.login()
        for name in ("dashboard_home", "dashboard_projects_view", "add_project", "messages", "subscriptions", "testimonials"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_create_project(self):
        self.login()
        resp = self.client.post(reverse("add_project"), {
            "title": "New thing", "description": "Hello", "category": "web", "status": "Live",
            "tech_stack": "Python", "highlights": "One\nTwo", "featured": "on",
        })
        self.assertRedirects(resp, reverse("dashboard_projects_view"))
        p = Project.objects.get(title="New thing")
        self.assertTrue(p.featured)
        self.assertEqual(p.highlight_list, ["One", "Two"])

    def test_create_project_requires_title(self):
        self.login()
        resp = self.client.post(reverse("add_project"), {"title": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_project_is_post_only(self):
        self.login()
        p = Project.objects.create(title="Gone soon")
        self.assertEqual(self.client.get(reverse("delete_project", args=[p.pk])).status_code, 405)
        self.assertTrue(Project.objects.filter(pk=p.pk).exists())
        resp = self.client.post(reverse("delete_project", args=[p.pk]))
        self.assertRedirects(resp, reverse("dashboard_projects_view"))
        self.assertFalse(Project.objects.filter(pk=p.pk).exists())

    def test_delete_requires_login(self):
        p = Project.objects.create(title="Keep me")
        resp = self.client.post(reverse("delete_project", args=[p.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Project.objects.filter(pk=p.pk).exists())

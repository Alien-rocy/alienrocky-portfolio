from django.db import models

# Create your models here.

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'Artificial Intelligence'),
        ('web', 'Web Development'),
        ('design', 'Design'),
        ('uiux', 'UI/UX Design'),
    ]

    title = models.CharField(max_length=200) 
    description = models.TextField(blank=True, null=True) 
    image = models.ImageField(upload_to="projects/", blank=True, null=True) 
    category = models.CharField(max_length=100, blank=True, null=True) 
    github_link = models.URLField(blank=True, null=True) 
    live_demo = models.URLField(blank=True, null=True)
    # Shown on the home page "Featured projects" section
    featured = models.BooleanField(default=False, help_text="Show on the home page")
    status = models.CharField(max_length=60, blank=True, default="", help_text="e.g. Live, In development, Prototype / MVP")
    tech_stack = models.CharField(max_length=200, blank=True, default="", help_text="Comma separated, e.g. Python, Django, PostgreSQL")
    highlights = models.TextField(blank=True, default="", help_text="One highlight per line")

    def __str__(self):
        return self.title

    @property
    def stack_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @property
    def highlight_list(self):
        return [l.strip() for l in self.highlights.splitlines() if l.strip()]

    @property
    def status_key(self):
        s = (self.status or "").lower()
        if "dev" in s or "progress" in s:
            return "dev"
        if "proto" in s or "mvp" in s or "beta" in s:
            return "proto"
        return "live"


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)  # ✅ approved by default

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

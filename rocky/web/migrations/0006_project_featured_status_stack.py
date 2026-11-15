from django.db import migrations, models

SEED = [
    {
        "title": "StudentPal",
        "category": "Academic Resource Platform",
        "status": "Built",
        "tech_stack": "Python, Django",
        "description": "An academic resource platform for the Faculty of Computing at Adekunle Ajasin University, Akungba-Akoko. Students get one place for notes, assignments, announcements and opportunities.",
        "highlights": "Notes, assignments, announcements and opportunities in one place\nBuilt for the Faculty of Computing, AAUA",
    },
    {
        "title": "Camply",
        "category": "Campus Mobility & Errand Platform",
        "status": "In development",
        "tech_stack": "Python, Django, JavaScript, PWA",
        "description": "A campus mobility and errand platform that makes everyday campus tasks easier through ride requests, errands and delivery services. The delivery and errand side is the part built so far.",
        "highlights": "Built: delivery and errand orders, customer accounts and a staff dashboard\nBuilt: installable PWA frontend (vanilla JS)\nPlanned: ride requests",
    },
    {
        "title": "ServeFlow",
        "category": "Restaurant Ordering System",
        "status": "Prototype / MVP",
        "tech_stack": "Python, Django, DRF, PostgreSQL",
        "description": "An API-first, multi-restaurant ordering system designed to improve how restaurants take orders and run service. Currently a working prototype heading toward an MVP.",
        "highlights": "Multi-restaurant (multi-tenant) architecture with per-restaurant staff access\nGuest ordering, pickup or dine-in, order status separate from payment status\nCustomer menu, restaurant dashboard and platform-owner dashboard",
    },
]


def seed(apps, schema_editor):
    Project = apps.get_model("web", "Project")
    for item in SEED:
        obj = Project.objects.filter(title__iexact=item["title"]).first()
        if obj is None:
            Project.objects.create(featured=True, **item)
        else:  # already added by hand: just feature it, keep your text
            obj.featured = True
            obj.save(update_fields=["featured"])


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0005_alter_testimonial_approved"),
    ]

    operations = [
        migrations.AddField(model_name="project", name="featured", field=models.BooleanField(default=False, help_text="Show on the home page")),
        migrations.AddField(model_name="project", name="status", field=models.CharField(blank=True, default="", help_text="e.g. Live, In development, Prototype / MVP", max_length=60)),
        migrations.AddField(model_name="project", name="tech_stack", field=models.CharField(blank=True, default="", help_text="Comma separated, e.g. Python, Django, PostgreSQL", max_length=200)),
        migrations.AddField(model_name="project", name="highlights", field=models.TextField(blank=True, default="", help_text="One highlight per line")),
        migrations.RunPython(seed, unseed),
    ]

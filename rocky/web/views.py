<<<<<<< HEAD
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from web.models import Project, Subscription, ContactMessage
from .forms import ProjectForm
from .models import ContactMessage
from .forms import ContactMessageForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Project, Subscription, Message, Testimonial
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages as flash
from django.core import signing
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging
import re
=======

import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.views.decorators.http import require_POST

from xhtml2pdf import pisa

from .forms import ProjectForm, ContactMessageForm
from .models import (
    Project,
    Subscription,
    ContactMessage,
    Testimonial,
)
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
from .portfolio_data import STACK, SKILL_GROUPS, ACHIEVEMENTS


logger = logging.getLogger(__name__)

# Email configuration
ADMIN_EMAIL = getattr(
    settings,
    "PORTFOLIO_NOTIFICATION_EMAIL",
    "rockytim5205@gmail.com",
)

<<<<<<< HEAD
def unsubscribe_link(request, email):
    """Absolute unsubscribe URL carrying a signed token (so nobody can unsubscribe other people)."""
    token = signing.dumps(email, salt="unsubscribe")
    return request.build_absolute_uri(f"/unsubscribe/{token}/")


def _notify(subject, message):
    """Email the site owner. Never raises: a mail problem must not break a page."""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_RECIPIENT])
    except Exception:
        logger.exception("Notification email failed: %s", subject)
=======
DEFAULT_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", None)
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9


# ==========================================================
# PUBLIC PAGES
# ==========================================================

def index(request):
<<<<<<< HEAD
    return render(request, "home.html", {
        "featured_projects": Project.objects.filter(featured=True).order_by("id"),
=======
    featured_projects = Project.objects.filter(
        featured=True
    ).order_by("id")

    return render(request, "Index.html", {
        "featured_projects": featured_projects,
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
        "stack_groups": STACK,
        "skill_groups": SKILL_GROUPS,
        "achievements": ACHIEVEMENTS,
    })


def About(request):
    """Keep the old About URL working."""
    return redirect("/#about")


def Projects(request):
    projects = list(Project.objects.all())

    # Prevent localhost URLs from appearing as public demos.
    for project in projects:
        demo = (project.live_demo or "").strip()

        if "127.0.0.1" in demo or "localhost" in demo:
            project.public_demo = ""
        else:
            project.public_demo = demo

    testimonials_list = Testimonial.objects.filter(
        approved=True
    ).order_by("-created_at")

    paginator = Paginator(testimonials_list, 5)
    testimonials = paginator.get_page(request.GET.get("page"))

    return render(request, "projects.html", {
        "projects": projects,
        "testimonials": testimonials,
        "total_testimonials": testimonials_list.count(),
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(request, "project_detail.html", {
        "project": project,
    })


# ==========================================================
# AUTHENTICATION
# ==========================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard_home")

        return render(request, "login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "login.html")


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


# ==========================================================
# CONTACT MESSAGES
# ==========================================================

def contact(request):
    if request.method != "POST":
        return redirect("/#contact")

<<<<<<< HEAD
            sender_email = contact_message.email.strip().lower()
            # Saved already; the email is only a notification.
            _notify(
                f"New Contact from {contact_message.name}",
                f"Email: {sender_email}\n\nMessage:\n{contact_message.message}",
            )
=======
    form = ContactMessageForm(request.POST)
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9

    if not form.is_valid():
        errors = {
            field: error_list[0]
            for field, error_list in form.errors.items()
        }

        return JsonResponse({
            "ok": False,
            "message": "Please fix the highlighted fields.",
            "errors": errors,
        }, status=400)

    # Save before attempting email notification.
    contact_message = form.save()

    try:
        send_mail(
            subject=f"New Contact from {contact_message.name}",
            message=(
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n\n"
                f"Message:\n{contact_message.message}"
            ),
            from_email=DEFAULT_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=False,
        )

    except Exception:
        logger.exception("Contact notification email failed.")

    return JsonResponse({
        "ok": True,
        "message": "Message sent successfully!",
    })


# ==========================================================
# DASHBOARD HOME
# ==========================================================

@login_required
def dashboard_home(request):
    testimonials = Testimonial.objects.all()

    return render(request, "dashboard/home.html", {
<<<<<<< HEAD
        "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
        "approved_count": testimonials.filter(approved=True).count(),
        "pending_count": testimonials.filter(approved=False).count(),
        "pending_testimonials": testimonials.filter(approved=False).order_by("-created_at")[:5],
        "projects": projects,
        "subscriptions": subscriptions,
        "contact_messages": messages,
        'testimonials': testimonials,
    })

def _save_project_form(request, form, success_text):
    """Validate + save a ProjectForm. Returns True on success; puts friendly errors on the form."""
    if not form.is_valid():
        return False
    uploading = bool(request.FILES.get("image"))
    if uploading and settings.ON_VERCEL and not settings.CLOUDINARY_ENABLED:
        form.add_error("image", "Image uploads need CLOUDINARY_URL to be set in Vercel's environment variables.")
        return False
    try:
        form.save()
    except Exception:
        logger.exception("Project could not be saved")
        form.add_error(None, "The project could not be saved. Check the image and try again.")
        return False
    flash.success(request, success_text)
    return True

=======
        "recent_messages": ContactMessage.objects.order_by(
            "-created_at"
        )[:5],

        "approved_count": testimonials.filter(
            approved=True
        ).count(),

        "pending_count": testimonials.filter(
            approved=False
        ).count(),

        "pending_testimonials": testimonials.filter(
            approved=False
        ).order_by("-created_at")[:5],

        "projects": Project.objects.all(),
        "subscriptions": Subscription.objects.all(),
        "messages": ContactMessage.objects.all(),
        "testimonials": testimonials,
    })


# ==========================================================
# PROJECT MANAGEMENT
# ==========================================================
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
<<<<<<< HEAD
        if _save_project_form(request, form, "Project added."):
            return redirect("dashboard_projects_view")
=======

        if form.is_valid():
            form.save()
            return redirect("dashboard_home")

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
    else:
        form = ProjectForm()

    return render(request, "dashboard/add_project.html", {
        "form": form,
    })



@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
<<<<<<< HEAD
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if _save_project_form(request, form, "Project updated."):
            return redirect("dashboard_projects_view")
=======
        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project,
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard_projects_view")

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
    else:
        form = ProjectForm(instance=project)

    return render(request, "dashboard/edit_project.html", {
        "form": form,
        "project": project,
    })



@login_required
@require_POST
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    title = project.title
    if project.image:
        try:
            project.image.delete(save=False)  # also removes the Cloudinary copy
        except Exception:
            logger.exception("Could not remove the image of project %s", pk)
    project.delete()
<<<<<<< HEAD
    flash.success(request, f"“{title}” was deleted.")
    return redirect("dashboard_projects_view")

=======

    return redirect("dashboard_projects_view")


@login_required
def dashboard_projects_view(request):
    projects = Project.objects.all().order_by("-id")

    return render(request, "dashboard/projects.html", {
        "projects": projects,
    })


# ==========================================================
# SUBSCRIPTIONS
# ==========================================================

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
@login_required
def subscriptions_view(request):
    subscriptions = Subscription.objects.all().order_by(
        "-created_at"
    )

    return render(request, "dashboard/subscriptions.html", {
        "subscriptions": subscriptions,
    })


@require_POST
def subscribe(request):
<<<<<<< HEAD
    if request.method != "POST":
        return JsonResponse({"message": "⚠️ Invalid request."}, status=405)
    email = (request.POST.get("email") or "").strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"message": "⚠️ Please enter a valid email address."}, status=400)

    sub, created = Subscription.objects.get_or_create(email=email)
    if not created:
        return JsonResponse({"message": "⚠️ You are already subscribed!"})

    _notify("New Subscription", f"A new subscriber joined: {email}")
    try:  # the subscription is saved even if the welcome email can't be sent
        html_content = render_to_string("emails/welcome.html", {
            "email": email,
            "unsubscribe_url": unsubscribe_link(request, email),
        })
        msg = EmailMultiAlternatives(
            "Welcome to Alien_R Newsletter",
            "Thanks for subscribing! You'll receive updates on new projects and testimonials.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception:
        logger.exception("Welcome email to %s failed", email)
    return JsonResponse({"message": "✅ Subscription successful!"})
=======
    email = request.POST.get("email", "").strip().lower()

    if not email:
        return JsonResponse({
            "message": "Please provide your email address."
        }, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "message": "Please provide a valid email address."
        }, status=400)

    subscription, created = Subscription.objects.get_or_create(
        email=email
    )

    if not created:
        return JsonResponse({
            "message": "You are already subscribed!"
        })

    # Notify the portfolio owner.
    try:
        send_mail(
            subject="New Subscription",
            message=f"A new subscriber joined: {email}",
            from_email=DEFAULT_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Subscription notification email failed.")

    # Send the welcome email independently.
    try:
        subject = "Welcome to Alien_R Newsletter"

        html_content = render_to_string(
            "emails/welcome.html",
            {"email": email},
        )

        text_content = (
            "Thanks for subscribing! "
            "You'll receive updates on new projects and testimonials."
        )

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=DEFAULT_EMAIL,
            to=[email],
        )

        email_message.attach_alternative(
            html_content,
            "text/html",
        )

        email_message.send(fail_silently=False)

    except Exception:
        logger.exception("Welcome email delivery failed.")

    return JsonResponse({
        "message": "Subscription successful!"
    })

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9

@login_required
@require_POST
def delete_subscription(request, pk):
<<<<<<< HEAD
    sub = get_object_or_404(Subscription, pk=pk)
    sub.delete()
    flash.success(request, "Subscriber removed.")
    return redirect("subscriptions")


@login_required
def messages_view(request):
    msgs = ContactMessage.objects.all()
    return render(request, "dashboard/messages.html", {"contact_messages": msgs})

@login_required
@require_POST
def delete_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    flash.success(request, "Message deleted.")
    return redirect("messages")
@login_required
def dashboard_projects_view(request):
    projects = Project.objects.all()
    return render(request, "dashboard/projects.html", {"projects": projects})
=======
    subscription = get_object_or_404(Subscription, pk=pk)
    subscription.delete()

    return redirect("subscriptions")


def unsubscribe(request, email):
    email = email.strip().lower()

    if request.method != "POST" and request.method != "GET":
        return HttpResponse(status=405)
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9

    deleted, _ = Subscription.objects.filter(
        email=email
    ).delete()

<<<<<<< HEAD



def add_testimonial(request):
    projects = Project.objects.all()
    testimonials_list = Testimonial.objects.filter(approved=True).order_by('-created_at')
    paginator = Paginator(testimonials_list, 5)
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)

    total_testimonials = testimonials_list.count()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        bad_words = [
            "spam", "fake", "scam", "fraud", "hate", "bad", "terrible", "awful",
            "useless", "worthless", "stupid", "idiot", "dumb", "nonsense",
            "trash", "garbage", "horrible", "worst", "pathetic", "ugly",
            "fool", "shame", "disgusting", "annoying", "boring", "lame",
            "cheat", "lying", "liar", "dangerous", "toxic", "abuse",
            "curse", "swear", "damn", "hell", "sucks", "loser"
        ]

        message = (message or "").strip()
        name = (name or "").strip()
        if not name or not message:
            return JsonResponse({"status": "Error", "message": "Name and review are required."}, status=400)

        words = set(re.findall(r"[a-z']+", message.lower()))  # whole words ("hello" is not "hell")
        approved_status = not (words & set(bad_words))

        testimonial = Testimonial.objects.create(
            name=name,
            email=email,
            message=message,
            approved=approved_status
        )

        # If AJAX request, return JSON
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
=======
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        if deleted:
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
            return JsonResponse({
                "message": "You have been unsubscribed."
            })

        return JsonResponse({
            "message": "Subscription not found."
        }, status=404)

    if deleted:
        # These names match the existing uploaded templates.
        return render(request, "unsubscribe_succes.html", {
            "email": email,
        })

    return render(request, "unsubscribe._fail.html", {
        "email": email,
    })


# ==========================================================
# CONTACT MESSAGE MANAGEMENT
# ==========================================================

@login_required
def messages_view(request):
    messages = ContactMessage.objects.all().order_by(
        "-created_at"
    )

    return render(request, "dashboard/messages.html", {
        "messages": messages,
    })


@login_required
def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    return render(request, "message_detail.html", {
        "msg": message,
    })

<<<<<<< HEAD
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")  # send user back to login page

@login_required
@require_POST
=======

@login_required
@require_POST
def delete_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()

    return redirect("messages")


# ==========================================================
# TESTIMONIAL MANAGEMENT
# ==========================================================

@login_required
def testimonials_view(request):
    testimonials = Testimonial.objects.all().order_by(
        "-created_at"
    )

    return render(request, "testimonials.html", {
        "testimonials": testimonials,
    })


def add_testimonial(request):
    if request.method != "POST":
        return redirect("Projects")

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip().lower()
    message = request.POST.get("message", "").strip()

    errors = {}

    if not name:
        errors["name"] = "Please enter your name."
    elif len(name) > 100:
        errors["name"] = "Name cannot exceed 100 characters."

    if email:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Please enter a valid email address."

    if not message:
        errors["message"] = "Please enter your review."

    if errors:
        return JsonResponse({
            "ok": False,
            "message": "Please correct the errors.",
            "errors": errors,
        }, status=400)

    # All public testimonials require dashboard approval.
    testimonial = Testimonial.objects.create(
        name=name,
        email=email or None,
        message=message,
        approved=False,
    )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "ok": True,
            "name": testimonial.name,
            "message": testimonial.message,
            "created_at": testimonial.created_at.strftime("%b %d, %Y"),
            "status": "Pending approval",
        })

    return redirect("Projects")


@login_required
@require_POST
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
def approve_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)

    testimonial.approved = True
<<<<<<< HEAD
    testimonial.save()
    flash.success(request, "Review approved.")
=======
    testimonial.save(update_fields=["approved"])

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
    return redirect("testimonials")


@login_required
@require_POST
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
<<<<<<< HEAD
    flash.success(request, "Review deleted.")
=======

>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
    return redirect("testimonials")


def all_testimonials(request):
    testimonials = Testimonial.objects.filter(
        approved=True
    ).order_by("-created_at")

    return render(request, "all_testimonials.html", {
        "testimonials": testimonials,
    })


# ==========================================================
# TESTIMONIAL API / LOAD MORE
# ==========================================================

def load_more_testimonials(request):
    testimonials = Testimonial.objects.filter(
        approved=True
    ).order_by("-created_at")

    paginator = Paginator(testimonials, 5)
    page = paginator.get_page(request.GET.get("page", 1))

<<<<<<< HEAD
    return JsonResponse({"testimonials": data, "has_next": paginator.get_page(page).has_next()})




def generate_portfolio_pdf(request):
    projects = Project.objects.all()
    testimonials = Testimonial.objects.filter(approved=True)
    template = get_template("portfolio_pdf.html")
    html = template.render({"projects": projects, "testimonials": testimonials})
    try:
        from xhtml2pdf import pisa  # imported lazily: keeps cold starts fast and the site up if it fails
    except ImportError:
        logger.exception("xhtml2pdf is not available")
        return HttpResponse("PDF export is temporarily unavailable.", status=503)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=portfolio.pdf"
    pisa.CreatePDF(html, dest=response)
    return response


def unsubscribe(request, token):
    try:
        email = signing.loads(token, salt="unsubscribe")
    except signing.BadSignature:
        return render(request, "unsubscribe_fail.html", {"email": "this address"}, status=400)
    deleted, _ = Subscription.objects.filter(email=email).delete()
    if deleted:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"message": "✅ You have been unsubscribed."})
        return render(request, "unsubscribe_success.html", {"email": email})
    return render(request, "unsubscribe_fail.html", {"email": email})
=======
    data = [
        {
            "message": testimonial.message,
            "name": testimonial.name,
            "created_at": testimonial.created_at.strftime("%b %d, %Y"),
        }
        for testimonial in page
    ]

    return JsonResponse({
        "testimonials": data,
        "has_next": page.has_next(),
    })


def testimonials_api(request):
    testimonials_list = Testimonial.objects.filter(
        approved=True
    ).order_by("-created_at")

    paginator = Paginator(testimonials_list, 5)
    page = paginator.get_page(request.GET.get("page", 1))

    data = [
        {
            "name": testimonial.name,
            "message": testimonial.message,
            "created_at": testimonial.created_at.strftime("%b %d, %Y"),
        }
        for testimonial in page
    ]

    return JsonResponse({
        "testimonials": data,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "page": page.number,
        "total_pages": paginator.num_pages,
    })


# ==========================================================
# PORTFOLIO PDF
# ==========================================================

def generate_portfolio_pdf(request):
    projects = Project.objects.all()
    testimonials = Testimonial.objects.filter(
        approved=True
    ).order_by("-created_at")

    try:
        template = get_template("portfolio_pdf.html")

        html = template.render({
            "projects": projects,
            "testimonials": testimonials,
        })

        response = HttpResponse(
            content_type="application/pdf"
        )

        response["Content-Disposition"] = (
            'attachment; filename="portfolio.pdf"'
        )

        result = pisa.CreatePDF(
            html,
            dest=response,
        )

        if result.err:
            logger.error("Portfolio PDF generation failed.")
            return HttpResponse(
                "Unable to generate portfolio PDF.",
                status=500,
            )

        return response

    except Exception:
        logger.exception("Portfolio PDF generation failed.")

        return HttpResponse(
            "Unable to generate portfolio PDF.",
            status=500,
        )
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9

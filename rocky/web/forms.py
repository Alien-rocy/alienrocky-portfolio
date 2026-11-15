# dashboard/forms.py
from django import forms
from web.models import Project, Subscription, ContactMessage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "image", "category", "status", "tech_stack", "highlights", "featured", "github_link", "live_demo"]
        widgets = {"image": forms.FileInput(attrs={"accept": "image/*"})}

    def clean_image(self):
        image = self.cleaned_data.get("image")
        # Vercel rejects request bodies over ~4.5 MB, so refuse oversized files politely.
        if image and hasattr(image, "size") and image.size > 4 * 1024 * 1024:
            raise forms.ValidationError("Image is larger than 4 MB. Choose a smaller image.")
        return image

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["email"]

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

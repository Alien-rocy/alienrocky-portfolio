"""
Media storage for hosts with a read-only filesystem (e.g. Vercel).

New uploads go to Cloudinary (reads CLOUDINARY_URL from the environment).
Images that already exist under MEDIA_ROOT (committed in the repo) are still
served locally, so older projects keep their screenshots.
"""
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):
    def _clean(self, name):
        return name.replace("\\", "/").lstrip("/")

    def get_available_name(self, name, max_length=None):
        # Random suffix keeps names unique without asking Cloudinary.
        root, ext = os.path.splitext(self._clean(name))
        return f"{root}_{get_random_string(7)}{ext}"

    def _save(self, name, content):
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(secure=True)
        name = self._clean(name)
        public_id = os.path.splitext(name)[0]
        if hasattr(content, "seek"):
            content.seek(0)
        cloudinary.uploader.upload(
            content, public_id=public_id, resource_type="image", overwrite=False
        )
        return name

    def _open(self, name, mode="rb"):
        raise NotImplementedError("Remote images are served by URL and are not opened by Django.")

    def exists(self, name):
        return False

    def delete(self, name):
        name = self._clean(name)
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return  # committed in the repo; leave it alone
        try:
            import cloudinary
            import cloudinary.uploader

            cloudinary.config(secure=True)
            cloudinary.uploader.destroy(os.path.splitext(name)[0], resource_type="image")
        except Exception:
            pass  # a failed remote delete should never break the dashboard

    def url(self, name):
        name = self._clean(name)
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return settings.MEDIA_URL + name
        import cloudinary
        import cloudinary.utils

        cloudinary.config(secure=True)
        return cloudinary.utils.cloudinary_url(os.path.splitext(name)[0], secure=True)[0]

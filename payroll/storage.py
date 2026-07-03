import os
import requests
from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, option=None):
        self.bucket = "media"
        # Extract from settings
        self.supabase_url = getattr(settings, 'SUPABASE_URL', '')
        self.supabase_key = getattr(settings, 'SUPABASE_KEY', '')

    def _open(self, name, mode='rb'):
        # We don't need opening stream support for writing to database,
        # but Django requires it. Let's fetch from public URL if needed.
        url = self.url(name)
        response = requests.get(url)
        if response.status_code == 200:
            import io
            return io.BytesIO(response.content)
        raise FileNotFoundError(f"File not found on Supabase: {name}")

    def _save(self, name, content):
        # Normalize path slashes for URL matching
        name = name.replace('\\', '/')
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{name}"
        
        headers = {
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": getattr(content, 'content_type', 'application/octet-stream')
        }

        content.seek(0)
        file_data = content.read()

        # Perform upload
        response = requests.post(upload_url, headers=headers, data=file_data)
        if response.status_code not in [200, 201]:
            # Fallback to PUT if file already exists
            response = requests.put(upload_url, headers=headers, data=file_data)
            if response.status_code not in [200, 201]:
                raise Exception(f"Supabase Storage Upload failed (Status {response.status_code}): {response.text}")

        return name

    def url(self, name):
        name = name.replace('\\', '/')
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{name}"

    def exists(self, name):
        name = name.replace('\\', '/')
        check_url = f"{self.supabase_url}/storage/v1/object/info/public/{self.bucket}/{name}"
        response = requests.get(check_url)
        return response.status_code == 200

    def size(self, name):
        return 0

from supabase import create_client
from django.conf import settings
from uuid import uuid4

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_file_to_supabase(file, path="uploads"):
    file_data = file.read()
    unique_name = f"{uuid4().hex}_{file.name}"
    file_path = f"{path}/{unique_name}"
    try:
        supabase.storage.from_(settings.SUPABASE_BUCKET).upload(file_path, file_data, {
            "content-type": file.content_type,
            "x-upsert": "true"
        })
    except Exception as e:
        return {"error": str(e)}

    public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_path)
    return {
        "file_path": file_path,
        "public_url": public_url
    }


def get_supabase_public_url(path):
    return f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{path}"

def delete_file_from_supabase(file_url):
    from urllib.parse import urlparse

    bucket_name = settings.SUPABASE_BUCKET
    base_path = urlparse(settings.SUPABASE_URL).netloc
    object_path = urlparse(file_url).path

    object_key = object_path.split(f"/storage/v1/object/public/{bucket_name}/")[-1]

    supabase.storage.from_(bucket_name).remove([object_key])
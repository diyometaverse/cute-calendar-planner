import os
import mimetypes
import environ
from supabase import create_client
env = environ.Env()
environ.Env.read_env()

SUPABASE_URL = env("SUPABASE_URL")
SUPABASE_KEY = env("SUPABASE_KEY")
SUPABASE_BUCKET = env("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

STATICFILES_DIR = os.path.join(os.getcwd(), 'staticfiles')

def upload_directory_to_supabase():
    for root, dirs, files in os.walk(STATICFILES_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, STATICFILES_DIR)
            supabase_path = f"static/{relative_path.replace(os.sep, '/')}"

            with open(local_path, "rb") as file_data:
                mime_type, _ = mimetypes.guess_type(filename)
                try:
                    print(f"Uploading: {supabase_path}")
                    supabase.storage.from_(SUPABASE_BUCKET).upload(
                        path=supabase_path,
                        file=file_data.read(),
                        file_options={
                            "content-type": mime_type or "application/octet-stream",
                            "x-upsert": "true"
                        }
                    )
                except Exception as e:
                    print(f"❌ Error uploading {filename}: {e}")

if __name__ == "__main__":
    upload_directory_to_supabase()

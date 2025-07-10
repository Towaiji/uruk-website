import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPA_PROJECT_URL")
SUPABASE_KEY = os.environ.get("SUPA_API_KEY")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

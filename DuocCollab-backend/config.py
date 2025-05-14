import os
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# Variables de configuración
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def headerApi():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }


def table_url(table_name: str) -> str:
    return f"{SUPABASE_URL}/rest/v1/{table_name}?select=*"


API_TOKEN = os.getenv("API_TOKEN")
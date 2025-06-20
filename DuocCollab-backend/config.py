import os
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()


class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    #hours=1
    #minutes

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

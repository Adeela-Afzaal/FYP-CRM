import logging
import os
import time
import threading
import requests
import psycopg2
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, EmailStr, Field
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

# CORS configuration
origins = ["https://localhost:7155"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants and configurations
VERIFY_TOKEN = "mindspark"
DATABASE_URL = "postgresql://postgres:adeela@localhost/FYP"
FACEBOOK_TOKEN_DB_URL = "postgresql://postgres:Ayesha253@localhost/FacebookTokens"

# Database connection
def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# ======================== Models ========================
class TokenData(BaseModel):
    AccessToken: str = Field(..., alias="accessToken")

class Message(BaseModel):
    id: str
    sender_id: str
    text: str

class SignUpModel(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

# ======================== Facebook/Instagram Integration ========================
def get_drive_service():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/drive']
    )
    creds.refresh(requests.Request())
    return build('drive', 'v3', credentials=creds)

# ======================== Routes ========================
@app.post("/api/facebook/save-token")
async def save_facebook_tokens(data: TokenData):
    if not data.AccessToken:
        raise HTTPException(status_code=400, detail="No access token provided")

    try:
        url = f"https://graph.facebook.com/me/accounts?access_token={data.AccessToken}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve pages")

        pages = response.json().get("data", [])
        if not pages:
            raise HTTPException(status_code=404, detail="No pages found")

        conn = psycopg2.connect(FACEBOOK_TOKEN_DB_URL)
        cur = conn.cursor()
        for page in pages:
            cur.execute("""
                INSERT INTO facebook_tokens (page_id, page_name, page_access_token, user_access_token)
                VALUES (%s, %s, %s, %s)
            """, (page.get("id"), page.get("name"), page.get("access_token"), data.AccessToken))
        conn.commit()
        return {"message": "Page access tokens saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), caption: str = Form(...)):
    try:
        # Save and upload file to Google Drive
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        drive_service = get_drive_service()
        file_metadata = {'name': file.filename}
        media = MediaFileUpload(file_path)
        
        drive_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        drive_service.permissions().create(
            fileId=drive_file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        public_url = f"https://drive.google.com/uc?export=download&id={drive_file['id']}"
        os.remove(file_path)
        return {"url": public_url, "caption": caption}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/post-to-instagram")
async def post_to_instagram(url: str, caption: str):
    try:
        INSTA_ACCESS_TOKEN = os.getenv('INSTA_ACCESS_TOKEN')
        INSTA_ACCOUNT_ID = os.getenv('INSTA_ACCOUNT_ID')
        
        # Create media container
        container_response = requests.post(
            f"https://graph.facebook.com/v18.0/{INSTA_ACCOUNT_ID}/media",
            params={'image_url': url, 'caption': caption, 'access_token': INSTA_ACCESS_TOKEN}
        )
        
        if container_response.status_code != 200:
            return {"error": "Container creation failed"}
        
        # Publish media
        publish_response = requests.post(
            f"https://graph.facebook.com/v18.0/{INSTA_ACCOUNT_ID}/media_publish",
            params={'creation_id': container_response.json().get('id'), 'access_token': INSTA_ACCESS_TOKEN}
        )
        
        if publish_response.status_code != 200:
            return {"error": "Publishing failed"}
        
        return {"success": True, "post_id": publish_response.json().get('id')}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ======================== User Authentication ========================
@app.post("/signup")
def signup(user: SignUpModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM "metaUsers" WHERE email = %s', (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        cursor.execute(
            'INSERT INTO "metaUsers" (username, email, password) VALUES (%s, %s, %s)',
            (user.name, user.email, user.password)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/login")
def login(user: LoginModel):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            'SELECT * FROM "metaUsers" WHERE email = %s AND password = %s',
            (user.email, user.password)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ======================== Server Startup ========================
def poll_messages():
    while True:
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=poll_messages, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
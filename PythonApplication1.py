# import logging  # Add this import statement at the top
# from fastapi import FastAPI, Form, UploadFile, File, Request,HTTPException,Body,BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import requests
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from pydantic.networks import import_email_validator
# import uvicorn
# from fastapi.responses import PlainTextResponse  # Import the PlainTextResponse
# import time
# import threading
# from threading import Thread
# from pydantic import BaseModel,EmailStr, Field
# from typing import List
# import email_validator
# from apscheduler.schedulers.background import BackgroundScheduler
# import asyncio



# app = FastAPI()
# logging.basicConfig(level=logging.DEBUG)

# # CORS configuration
# origins = [
#     "https://localhost:7155",  # Allow your Blazor WebAssembly app
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# VERIFY_TOKEN = "mindspark"
# PAGE_ACCESS_TOKEN="EAAF1YPkIddcBO2csAxn8c1ZCriwPrnbxCGxRZAa3rS6QnM9AjIlfrJ69OeKgPDsjk0gXD7NdwktjiSogY65Tgasj5eHq2mVCkmcLWRyC0zIsqQeewinZBunfkHJmENZCBRl62ZAEL9vydwVylfh88dZCZCyCfRxS4RrmWMMCq0xCfXzmssdABJpyu6UFVm3V1OK2wZDZD"
# PAGE_ID = '433410053193609'
# IG_ACCOUNT_ID = "17841470286947864"
# # PostgreSQL database connection
# def get_db_connection():
#     try:
#         conn = psycopg2.connect(
#             database="FYP",
#             user="postgres",
#             password="adeela",
#             host="localhost",
#             port="5432"
#         )
#         return conn
#     except Exception as e:
#         logging.error(f"Database connection error: {e}")
#         raise HTTPException(status_code=500, detail="Database connection error")
# #------------------------------Token Generation-----------------------------------
# DATABASE_URL = "postgresql://postgres:Ayesha253@localhost/FacebookTokens"
# class TokenData(BaseModel):
#     AccessToken: str=Field(..., alias="accessToken")
# @app.post("/api/facebook/save-token")
# async def save_facebook_tokens(data: TokenData):
#     # Log the received token to debug
#     print(f"Received Token: {data.AccessToken}")
#     if not data.AccessToken:
#         raise HTTPException(status_code=400, detail="No access token provided")
#     print("Access Token:", data.AccessToken)
#     # Ensure AccessToken is provided
    

#     # Fetch pages managed by the user
#     url = f"https://graph.facebook.com/me/accounts?access_token={data.AccessToken}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Failed to retrieve pages")

#     pages = response.json().get("data", [])
    
#     # Check if pages are retrieved
#     if not pages:
#         raise HTTPException(status_code=404, detail="No pages found")

#     # Connect to PostgreSQL and store page tokens
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cur = conn.cursor()

#         for page in pages:
#             page_id = page.get("id")
#             page_name = page.get("name")
#             page_access_token = page.get("access_token")

#             # Insert page details into database
#             cur.execute("""
#                 INSERT INTO facebook_tokens (page_id, page_name, page_access_token, user_access_token)
#                 VALUES (%s, %s, %s, %s)
                
#             """, (page_id, page_name, page_access_token, data.AccessToken))

#         conn.commit()
#         cur.close()
#         conn.close()

#         return {"message": "Page access tokens saved successfully"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# # ======================== Webhook Handlers ========================


# # Pydantic models for request and response
# class Message(BaseModel):
#     id: str
#     sender_id: str
#     text: str

# class SendMessageRequest(BaseModel):
#     recipient_id: str
#     message_text: str
# class SignUpModel(BaseModel):
#     name: str
#     email: EmailStr
#     password: str


# class LoginModel(BaseModel):
#     email: EmailStr
#     password: str


# messages = []#list to store messages
# # Endpoint to retrieve messages
# @app.get("/api/facebook/messages")
# def get_messages():
#     messages = get_new_messages()  # This should return a list of messages
#     return {"messages": messages}



# def get_new_messages():
#     url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/conversations"
#     params = {
#         'access_token': PAGE_ACCESS_TOKEN,
#         'fields': 'messages.limit(1){message,from}'  # Ensure to include 'from' for sender details
#     }
#     response = requests.get(url, params=params)
    
#     # Log the full response to inspect its structure
#     data = response.json()
#     print("API response:", data)
    
#     messages = []
#     if 'data' in data:
#         for conversation in data['data']:
#             messages_data = conversation.get('messages', {}).get('data', [])
#             if messages_data:
#                 # Extract sender's information
#                 last_message = messages_data[0]
#                 sender_id = last_message['from'].get('id')  # Sender's ID
#                 message_text = last_message.get('message')  # Message text
                
#                 # Log extracted data
#                 print(f"Sender ID: {sender_id}, Message Text: {message_text}")

#                 # Append to message list only if both values are not null
#                 if sender_id and message_text:
#                     messages.append({
#                         "senderId": sender_id, 
#                         "messageText": message_text
#                     })
#                 # Process the message (for example, if it's a new message, send a response)
#                 if 'hello' in message_text.lower():
#                       send_message(sender_id, "Hi! How can I assist you?")
    
    
#     return messages

# def send_message(recipient_id, message_text):
#     url = f"https://graph.facebook.com/v12.0/me/messages"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         'recipient': {'id': recipient_id},
#         'message': {'text': message_text},
#         'access_token': PAGE_ACCESS_TOKEN
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     return response.json()

# def poll_messages():
#     while True:
#         get_new_messages()
#         time.sleep(60)  # Poll every 60 seconds



# #----------------------------------Signup and login----------------------------------
# @app.post("/signup")
# def signup(user: SignUpModel):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         # Check if email already exists
#         cursor.execute('SELECT * FROM "metaUsers" WHERE email = %s', (user.email,))
#         if cursor.fetchone():
#             raise HTTPException(status_code=400, detail="Email already registered")

#         # Insert new user into the database
#         cursor.execute(
#             'INSERT INTO "metaUsers" (username, email, password) VALUES (%s, %s, %s)',
#             (user.name, user.email, user.password)
#         )
#         conn.commit()
#         logging.info(f"User {user.email} registered successfully.")
#         return {"message": "User registered successfully"}
#     except Exception as e:
#         conn.rollback()
#         logging.error(f"Error during signup: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()
#         conn.close()


# @app.post("/login")
# def login(user: LoginModel):
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     try:
#         cursor.execute(
#             'SELECT * FROM "metaUsers" WHERE email = %s AND password = %s',
#             (user.email, user.password)
#         )
#         db_user = cursor.fetchone()
#         if not db_user:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#         logging.info(f"User {user.email} logged in successfully.")
#         return {"message": "Login successful", "user": db_user}
#     except Exception as e:
#         logging.error(f"Error during login: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()
#         conn.close()
# @app.post("/post_image_to_facebook")
# async def post_image_to_facebook(image: UploadFile = File(...), caption: str = ""):
#     try:
#         # Read image data
#         image_data = await image.read()

#         # Define the Facebook Graph API endpoint and access token
#         access_token = "EAAF1YPkIddcBO2csAxn8c1ZCriwPrnbxCGxRZAa3rS6QnM9AjIlfrJ69OeKgPDsjk0gXD7NdwktjiSogY65Tgasj5eHq2mVCkmcLWRyC0zIsqQeewinZBunfkHJmENZCBRl62ZAEL9vydwVylfh88dZCZCyCfRxS4RrmWMMCq0xCfXzmssdABJpyu6UFVm3V1OK2wZDZD"
#         page_id = "433410053193609"  # Replace with your actual page ID
#         IG_ACCOUNT_ID = "17841470286947864"
#         url = f"https://graph.facebook.com/v12.0/{page_id}/photos"

#         # Prepare the payload for the POST request
#         payload = {
#             "message": caption,
#             "access_token": access_token
#         }

#         # Make the request to the Facebook Graph API
#         files = {
#             "file": (image.filename, image_data, image.content_type)
#         }

#         response = requests.post(url, data=payload, files=files)

#         # Check for a successful response
#         if response.status_code == 200:
#             return {"message": "Posted image successfully!", "data": response.json()}
#         else:
#             return JSONResponse(status_code=response.status_code, content={"message": "Failed to post image", "error": response.json()})

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})

# @app.post("/post_text_to_facebook")
# async def post_text_to_facebook(message: str = Form(...)):
#     try:
#         # Simulate posting to Facebook (replace this with actual API logic if needed)
#         return {"message": f"Posted text: {message}"}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})
    


# if __name__ == "__main__":
#     threading.Thread(target=poll_messages, daemon=True).start()
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, HTTPException
import os
from twilio.rest import Client
from dotenv import load_dotenv
import re
from db import init_db, add_activity
from scheduler import initialize_scheduler

# loading & defining environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_NUMBER = os.getenv("MY_PHONE_NUMBER")

# Initializing twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Helper functions

def parse_message(text: str):
    message = text.split()
    mood = int(message[-1])
    message.pop()
    activity = ' '.join(message)
    return activity, mood

scheduler = None

# lifespan (on startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting up!")
    init_db()
    global scheduler
    scheduler = initialize_scheduler(client, TWILIO_NUMBER, MY_NUMBER)
    yield
    scheduler.shutdown()
    print("App shutting down!")

def send_message(body):
    client.messages.create(from_=TWILIO_NUMBER,
                                body=f"{body}",
                                to=MY_NUMBER)

# initializing fastapi
app = FastAPI(lifespan=lifespan)

# Recieving message endpoint
@app.post('/sms')
def receive_sms(Body: str = Form()):
    try:
        if Body == 'sleep':
            add_activity("Sleeping", 10)
            send_message("Good night, Joseph!")
            scheduler.pause_job("prompt_job")
            return {'status': 'saved'}
        elif Body == 'awake':
            add_activity("Morning routine: prayer & bible", 10)
            send_message("Rise & Shine, win the day!")
            scheduler.resume_job("prompt_job")
            return {'status': 'saved'}
        activity, mood = parse_message(Body)
        add_activity(activity, mood)
    except:
        send_message("Please input format correctly")
        raise HTTPException(status_code=404, detail="Incorrect format")

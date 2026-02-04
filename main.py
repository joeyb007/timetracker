from fastapi import FastAPI, Form, HTTPException
import os
from twilio.rest import Client
from dotenv import load_dotenv
import re

# loading & defining environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_NUMBER = os.getenv("MY_PHONE_NUMBER")

# Initializing twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# initializing fastapi
app = FastAPI()

# Helper functions

def parse_message(text: str):
    message = text.split()
    mood = int(message[-1])
    message.pop()
    activity = ' '.join(message)
    return activity, mood

# Recieving message endpoint
@app.post('/sms')
def receive_sms(Body: str = Form()):
    try:
        activity, mood = parse_message(Body)
    except:
        client.messages.create(from_=TWILIO_NUMBER,
                                body="Please format input correctly",
                                to=MY_NUMBER)
        raise HTTPException(status_code=404, detail="Item not found")

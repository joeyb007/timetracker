from fastapi import FastAPI
import os
from twilio.rest import Client
from dotenv import load_dotenv

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


if __name__ == "__main__":
    message = client.messages.create(from_=TWILIO_NUMBER,
                                    body="Here's your text!",
                                    to=MY_NUMBER)

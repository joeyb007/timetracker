from fastapi import FastAPI
import os
from twilio.rest import Client


# setting up env vars

app = FastAPI()
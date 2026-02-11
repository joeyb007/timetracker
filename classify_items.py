import os
from dotenv import load_dotenv
from typing import List
from groq import Groq
import json
import http
import psycopg2

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv('DATABASE_URL')


def generate_activities():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT activity, activity_id FROM activities")
    rows = cursor.fetchall()
    connection.close()
    return rows

def build_prompt(activities: List[str]):
   prompt = f""" Over the following week, I completed the following activities:
                {"\n".join(f'- {a[0]}' for a in activities)}
                First, suggest 5-8 categories that would best group these activities.
                Then categorize each activity into one of those categories.

                Respond ONLY with valid JSON in this format:
                {{
                "categories": ["Category1", "Category2", ...],
                "classified": {{"activity1": "Category1", "activity2": "Category2", ...}}
                }}"""
   return prompt

def classify_activities(activities: List[str]):
    client = Groq(api_key=GROQ_API_KEY)
    PROMPT = build_prompt(activities)
    chat_completion = client.chat.completions.create(
    messages=[
            {
                "role": "user",
                "content": PROMPT,
            }
        ],
        model="groq/compound",
    )
    response = chat_completion.choices[0].message.content
    try:
        response = json.loads(response)
        categories = response["categories"]
        classification = response["classified"]
    except:
        print("LLM output not as expected")
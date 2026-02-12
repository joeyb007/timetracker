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


def build_prompt(activities: List[str]):
   prompt = f""" Over the following week, I completed the following activities:
                {"\n".join(f'- {a}' for a in activities)}
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
        model="llama-3.1-8b-instant",
    )
    response = chat_completion.choices[0].message.content
    try:
        result = json.loads(response)
        return result["classified"]
    except:
        print("LLM output not as expected")
        print(response)  # Print to see what went wrong
        return None

if __name__ == "__main__":
    import json

    with open("week_data.json", "r") as f:
        week_data = json.load(f)

    activities = set()
    for date, slots in week_data.items():
        for slot in slots:
            if slot:
                activities.add(slot["activity"])

    classified = classify_activities(list(activities))
    
    if classified:
        for date, slots in week_data.items():
            for slot in slots:
                if slot:
                    activity = slot["activity"]
                    if activity in classified:
                        slot["category"] = classified[activity]
        
        with open("week_data_classified.json", "w") as f:
            json.dump(week_data, f, indent=2)
        
        print("Done. Saved to week_data_classified.json")
    else:
        print("Classification failed")
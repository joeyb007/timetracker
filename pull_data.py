import psycopg2
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def get_data():
    res = []
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT activity, mood, timestamp FROM activities ORDER BY timestamp")
    rows = cursor.fetchall()
    connection.close()
    for row in rows:
        res.append(row)
    return res

def convert_to_eastern(timestamp_str):
    dt = datetime.fromisoformat(timestamp_str)
    dt_eastern = dt - timedelta(hours=5)
    return dt_eastern.isoformat()

def data_dictionary(rows):
    days_data = {}
    for row in rows:
        activity, mood, timestamp = row
        timestamp = convert_to_eastern(timestamp)
        date = timestamp[:10]
        
        if date not in days_data:
            days_data[date] = []
        
        days_data[date].append((timestamp, activity, mood))
    return days_data

def get_slot_index(timestamp):
    hour = int(timestamp[11:13])
    minute = int(timestamp[14:16])
    total_minutes = hour * 60 + minute
    slot = round(total_minutes / 30)
    return min(slot, 47)

def build_day_slots(entries):
    slots = [None] * 48
    entries = sorted(entries, key=lambda x: x[0])
    
    for i, (timestamp, activity, mood) in enumerate(entries):
        start_slot = get_slot_index(timestamp)
        
        if i + 1 < len(entries):
            end_slot = get_slot_index(entries[i + 1][0])
        else:
            end_slot = 48
        
        for s in range(start_slot, end_slot):
            slots[s] = {"activity": activity, "mood": mood, "category": "Other"}
    
    return slots

days_data = data_dictionary(get_data())

week_data = {}
for date, entries in days_data.items():
    week_data[date] = build_day_slots(entries)

with open("week_data.json", "w") as f:
    json.dump(week_data, f, indent=2)

print("Done. Days:", list(week_data.keys()))
import sqlite3
from datetime import datetime

def init_db():
    connection = sqlite3.connect("daily_actions.db")
    cursor = connection.cursor()
    command = "CREATE TABLE IF NOT EXISTS activities(activity_id INTEGER PRIMARY KEY," \
    "                                                activity TEXT," \
    "                                                mood INTEGER," \
    "                                                timestamp TEXT)"
    cursor.execute(command)
    connection.commit()
    connection.close()

def add_activity(activity, mood):
    current_time = datetime.now().isoformat()
    connection = sqlite3.connect("daily_actions.db")
    cursor = connection.cursor()
    cursor.execute(
    "INSERT INTO activities (activity, mood, timestamp) VALUES (?, ?, ?)",
    (activity, mood, current_time)
)
    connection.commit()
    connection.close()
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    command = "CREATE TABLE IF NOT EXISTS activities(activity_id SERIAL PRIMARY KEY," \
    "                                                activity TEXT," \
    "                                                mood INTEGER," \
    "                                                timestamp TEXT)"
    cursor.execute(command)
    connection.commit()
    connection.close()

def add_activity(activity, mood):
    current_time = datetime.now().isoformat()
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute(
    "INSERT INTO activities (activity, mood, timestamp) VALUES (%s, %s, %s)",
    (activity, mood, current_time)
)
    connection.commit()
    connection.close()
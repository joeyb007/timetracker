from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
def send_prompt(client, from_number, to_number):
    client.messages.create(from_=from_number,
                                body="Whatcha up to?",
                                to=to_number)

def initialize_scheduler(client, from_number, to_number):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_prompt, 'interval', minutes=30, args=(client, from_number, to_number), id="prompt_job", next_run_time=datetime.now())
    scheduler.start()
    print("Scheduler started!")
    return scheduler
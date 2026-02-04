from apscheduler.schedulers.background import BackgroundScheduler

def send_prompt(client, from_number, to_number):
    client.messages.create(from_=from_number,
                                body="Whatcha up to?",
                                to=to_number)

def initialize_scheduler(client, from_number, to_number):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_prompt, 'interval', minutes=1, args=(client, from_number, to_number))

    return scheduler
from time import sleep
from celery import shared_task

@shared_task
def notify_customers(message):
    print('seeding 10 messages')
    print(message)
    sleep(10)
    print("Emails were successfully sent to customers.")
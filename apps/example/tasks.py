from celery import shared_task
import time


@shared_task
def mul(x, y):
    time.sleep(2)
    return x * y

from datetime import datetime
import os
from scheduler import bonus_calculation
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bonus_calculation.calculate_bonus_test, 'interval', minutes=1)
    scheduler.start()

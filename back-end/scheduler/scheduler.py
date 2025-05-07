from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.update_game import run as update_games_job

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_games_job, 'cron', hour=3)
    scheduler.start()
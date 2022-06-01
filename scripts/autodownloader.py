from scripts.tables_downloader import start_up, download_du_active, download_request_active
from handlers.activity import update_activity
from threading import Thread
from time import sleep, strftime


def download():
    start_up()
    download_du_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: du downloaded successfully')
    download_request_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: request downloaded successfully')


def run_download():
    while True:
        sleep(28000)  # треть дня
        download()
        sleep(60)
        update_activity()


def scheduled_download():
    """Автоскачивание таблиц с расписанием, актисностью ИТИСа (реквест) и активностью ДУ18.
    Также обновление переменных с баллами студентов (rating, students)"""
    Thread(target=run_download).start()

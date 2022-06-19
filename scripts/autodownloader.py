from scripts.tables_downloader import start_up, download_du_active, download_request_active
from scripts.excel import reload_data
from handlers.activity import update_activity
from threading import Thread
from time import sleep, strftime


def download():
    start_up()
    download_du_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: du downloaded successfully', flush=True)
    download_request_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: request downloaded successfully', flush=True)


def run_download():
    while True:
        sleep(3600)  # один час
        download()
        reload_data()
        sleep(60)
        update_activity()


def scheduled_download():
    """Автоскачивание таблиц с расписанием, актисностью ИТИСа (реквест) и активностью ДУ18.
    Также обновление переменных с баллами студентов (rating, students)"""
    Thread(target=run_download).start()

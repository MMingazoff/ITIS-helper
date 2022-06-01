from scripts.tables_downloader import start_up, download_du_active, download_request_active  # , download_raskraska
# from scripts.timetable_editor import get_edit_timetable
from handlers.activity import update_activity
from threading import Thread
from time import sleep, strftime

# sheet = {'1 курс': '1course', '2 курс': '2course', '3 курс': '3course', '4 курс': '4course', 'Магистры': 'masters'}


def download():
    start_up()
    download_du_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: du downloaded successfully')
    download_request_active()
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: request downloaded successfully')
    # download_raskraska()
    # print(f'{strftime("%d-%m-%Y %H:%M:%S")}: timetable downloaded successfully')
    # get_edit_timetable(sheet)
    # print(f'{strftime("%d-%m-%Y %H:%M:%S")}: timetable edited successfully')


def run_download():
    while True:
        sleep(100)
        download()
        sleep(60)
        update_activity()


def scheduled_download():
    """Автоскачивание таблиц с расписанием, актисностью ИТИСа (реквест) и активностью ДУ18.
    Также обновление переменных с баллами студентов (rating, students)"""
    Thread(target=run_download).start()

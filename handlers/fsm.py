from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_start(StatesGroup):
    fio = State()
    menu = State()
    swap_profile =State()


class FSM_timetable(StatesGroup):
    timetable = State()
    today_tomorrow = State()
    someone_timetable = State()


class FSM_study(StatesGroup):
    study = State()
    subject = State()


class FSM_helps(StatesGroup):
    help = State()
    wishes = State()


class FSM_activity(StatesGroup):
    activity = State()
    activities = State()
    someone_points = State()
    top_students = State()


class FSM_guide(StatesGroup):
    guide = State()

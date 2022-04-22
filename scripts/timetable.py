def get_week_timetable(group: str) -> str:
    """Расписание на неделю"""
    text = 'Понедельник:' + '\n' + '8:30-10:00 Алгем' + '\n' + '10:10-11:40 Ифнорматика' + '\n' + '11:50-13:20 АиСД'
    return text


def get_now_lesson(group: str) -> str:
    """Какая сечас пара"""
    text = 'Сейчас у тебя Алгем в 109, преподователь Арсланов М.М. '
    return text


def get_today_lessons(group: str) -> str:
    text = '8:30-10:00 Алгем' + '\n' + '10:10-11:40 Математический анализ' + '\n' + '11:50-13:20 Информатика'
    return text


def get_tomorrow_lessons(group: str) -> str:
    text = '8:30-10:00 Алгем' + '\n' + '11:50-13:20' + 'АиСД'
    return text


def get_today_lessons_by_group(group: str):
    text = '8:30-10:00 Алгем' + '\n' + '10:10-11:40 Математический анализ' + '\n' + '11:50-13:20 Информатика'
    return text

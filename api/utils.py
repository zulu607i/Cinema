import datetime


def get_current_week():
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    return start_week, end_week


def get_next_week():
    date = datetime.date.today()
    start_week = date + datetime.timedelta(7)
    end_week = start_week + datetime.timedelta(7)
    return start_week, end_week


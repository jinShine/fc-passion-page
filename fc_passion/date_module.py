import datetime

def day_of_the_week(year, month, day):
    dayOfWeek = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return dayOfWeek[datetime.date(int(year), int(month), int(day)).weekday()]

def now():
    return datetime.datetime.now()
# get a datetime string in persian 'سه‌شنبه ۷ شهریور ۱۴۰۲ - ۲۳:۵۴' format and return georgian datetime object

from persiantools.jdatetime import JalaliDateTime
from unidecode import unidecode

MONTHS = {
    'فروردین': 1,
    'اردیبهشت': 2,
    'خرداد': 3,
    'تیر': 4,
    'مرداد': 5,
    'شهریور': 6,
    'مهر': 7,
    'آبان': 8,
    'آذر': 9,
    'دی': 10,
    'بهمن': 11,
    'اسفند': 12,
}


def converter(string):
    string_list = string.replace('- ', '').split(' ')
    hour, minute = string_list[-1].split(':')
    hour, minute = int(hour), int(minute)
    year = int(unidecode(string_list[-2]))
    month = MONTHS[string_list[-3]]
    day = int(unidecode(string_list[-4]))
    jalali_datetime = JalaliDateTime(year, month, day, hour, minute)
    return jalali_datetime.to_gregorian()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

MOIS = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre',
        u'novembre', u'décembre']

def date_to_fr_ca(dt):
    return str(dt.day) + ' ' + MOIS[dt.month-1] + ' ' + str(dt.year)

def json_date_as_datetime(jd):
    sign = jd[-7]
    if sign not in '-+' or len(jd) == 13:
        millisecs = int(jd[6:-2])
    else:
        millisecs = int(jd[6:-7])
        hh = int(jd[-7:-4])
        mm = int(jd[-4:-2])
        if sign == '-': mm = -mm
        millisecs += (hh * 60 + mm) * 60000
    return datetime.datetime(1970, 1, 1) \
        + datetime.timedelta(microseconds=millisecs * 1000)

def weekday(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    dayOfWeek  = 5
    dayOfWeek += (aux + afterFeb) * 365
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
    dayOfWeek += offset[month - 1] + (day - 1)
    dayOfWeek %= 7
    return dayOfWeek

def weekdaysbefore(ordinaldate):
    dt = datetime.datetime.fromordinal(ordinaldate)
    day = weekday(dt.year, dt.month, dt.day)
    days = []
    for i in reversed(range(1, day+1)):
        d = ordinaldate - i
        days.append(d)
    return days

def weekbefore(ordinaldate):
    dt = datetime.datetime.fromordinal(ordinaldate)
    if weekday(dt.year, dt.month, dt.day) == 0:
        days = weekdaysbefore(ordinaldate - 1)
        days.append(ordinaldate - 1)
        return days
    else:
        return weekdaysbefore(ordinaldate)

def currentweek(ordinaldate):
    dt = datetime.datetime.fromordinal(ordinaldate)
    sunday = ordinaldate - weekday(dt.year, dt.month, dt.day)
    days = []
    for i in range(7):
        days.append(sunday + i)
    return days

def nextweek(ordinaldate):
    dt = datetime.datetime.fromordinal(ordinaldate)
    nextsunday = ordinaldate - weekday(dt.year, dt.month, dt.day) + 7
    days = []
    for i in range(7):
        days.append(nextsunday + i)
    return days

if __name__ == "__main__":
    print 'This module is not intended to be run directly.'

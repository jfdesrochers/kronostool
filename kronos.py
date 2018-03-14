# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError, HTTPError
from time import sleep
from xml.etree import ElementTree as ET
from dateutil import parser
import pytz
import sys
import platform
import tempfile
import webbrowser
from timetools import currentweek, nextweek, weekday, date_to_fr_ca
from datetime import datetime, timedelta
from getpass import getpass, fallback_getpass
from kronossched import schedule
from template_engine import template
import os

if getattr(sys, 'frozen', False):
    app_path = getattr(sys, '_MEIPASS', os.getcwd())
elif __file__:
    app_path = os.path.dirname(os.path.realpath(__file__))
else:
    app_path = os.getcwd()

certpath = os.path.join(app_path, 'cacert.pem')
if os.path.isfile(certpath):
    os.environ['REQUESTS_CA_BUNDLE'] = certpath

week_parse = [
    [datetime.fromordinal(x) for x in currentweek(datetime.now().toordinal())],
    [datetime.fromordinal(x) for x in nextweek(datetime.now().toordinal())]
]

label_classes = ['yellow', 'pink', 'blue', 'green', 'orange', 'purple', 'light-blue', 'light-green', 'amber', 'teal',
                 'red', 'lime', 'deep-purple', 'deep-orange', 'indigo', 'cyan']

RETRIES = 5

base_url = 'https://mytimemobile.staples.com/wfc/bridge/'
login_data = '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\' ?><Logon username="{user}" password="{pwd}" ' \
             'appversion="4.00.00.064" />'
sched_data = '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\' ?><scheduleInitializationContext><dateRange>' \
             '<startDateUTC>{datefrom}</startDateUTC><endDateUTC>{dateto}</endDateUTC></dateRange><hyperfindId>' \
             '<value>1</value></hyperfindId><includeOpenShifts>true</includeOpenShifts>' \
             '<includeTransferedEmployees>true</includeTransferedEmployees>' \
             '<includeUserJobTransferSetOpenShifts>true</includeUserJobTransferSetOpenShifts>' \
             '</scheduleInitializationContext>'
kronos_headers = {'User-Agent': 'KronosMobile-Android',
                  'Accept': 'application/xml',
                  'Accept-Charset': 'UTF-8',
                  'Accept-Encoding': 'gzip;q=0.8, deflate;q=0.5',
                  'Content-Type': 'application/xml; charset=UTF-8',
                  'Connection': 'Keep-Alive'
                  }


def win_getpass(prompt='Password: ', stream=None):
    """Prompt for password with echo off, using Windows getch()."""
    if sys.stdin is not sys.__stdin__:
        return fallback_getpass(prompt, stream)
    import msvcrt

    for c in prompt:
        msvcrt.putch(c)
    pw = ""
    while 1:
        c = msvcrt.getch()
        if c == '\r' or c == '\n':
            break
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b':
            if pw == '':
                pass
            else:
                pw = pw[:-1]
                msvcrt.putch('\b')
                msvcrt.putch(" ")
                msvcrt.putch('\b')
        else:
            pw = pw + c
            msvcrt.putch("*")
    msvcrt.putch('\r')
    msvcrt.putch('\n')
    return pw


if platform.system() == 'Windows':
    getpass = win_getpass


def _pause(tottime):
    if tottime >= timedelta(hours=9):
        tottime = tottime - timedelta(hours=1)
    elif tottime > timedelta(hours=5):
        tottime = tottime - timedelta(minutes=30)
    h, r = divmod(tottime.seconds, 3600)
    m, s = divmod(r, 60)
    return (h, m, s)


def get_schedule(user, pwd, datefrom, dateto):
    s = requests.Session()
    s.headers = kronos_headers
    res = s.post(base_url + 'rest/logon', login_data.format(user=user, pwd=pwd))
    if res.status_code == 200:
        res = s.post(base_url + 'services/tokens/rest/1.0/createToken')
        if res.status_code == 200:
            res = s.post(base_url + 'schedulemanager/mobile/rest/1.0/schedules/' + res.text + '/init',
                         sched_data.format(datefrom='{:%Y-%m-%d}'.format(datefrom),
                                           dateto='{:%Y-%m-%d}'.format(dateto)))
            if res.status_code == 200:
                return res.text
            else:
                res.raise_for_status()
        else:
            res.raise_for_status()
    else:
        res.raise_for_status()


def parse_schedule(sched):
    root = ET.fromstring(sched.encode('utf-8'))
    staff_list = []
    emplist = root.find('employees')
    for emp in emplist:
        staff_list.append({'id': emp.find('personNumber').text,
                           'name': emp.find('fullName').text,
                           'job': emp.find('primaryJob').find('path').text,
                           'shifts': ['' for x in range(7)],
                           'labels': ['' for x in range(7)]})
    staff_list.sort(key=lambda k: k['name'])
    staff_list.sort(key=lambda k: k['job'])
    labels = {}
    jobcodes = root.find('payCodeEdits')
    for jobcode in jobcodes:
        assid = jobcode.find('employee').find('personNumber').text
        shiftstart = pytz.utc.normalize(parser.parse(jobcode.find('startDateTimeUTC').text).astimezone(pytz.utc))
        shiftlabel = jobcode.find('payCode').find('name').text
        for staff in staff_list:
            if staff['id'] == assid:
                shiftday = weekday(shiftstart.year, shiftstart.month, shiftstart.day)
                if shiftlabel is not None:
                    staff['labels'][shiftday] = shiftlabel
                    if shiftlabel not in labels and len(labels) <= 16:
                        labels[shiftlabel] = label_classes[len(labels)]
    shifts = root.find('shifts')
    for shift in shifts:
        assid = shift.find('employee').find('personNumber').text
        shiftstart = pytz.utc.normalize(parser.parse(shift.find('startDateTimeUTC').text).astimezone(pytz.utc))
        shiftend = pytz.utc.normalize(parser.parse(shift.find('endDateTimeUTC').text).astimezone(pytz.utc))
        shiftlabel = shift.find('label').text
        for staff in staff_list:
            if staff['id'] == assid:
                shiftday = weekday(shiftstart.year, shiftstart.month, shiftstart.day)
                staff['shifts'][shiftday] = '{:%H:%M}-{:%H:%M} ({hms[0]}h{hms[1]:02d})'.format(shiftstart, shiftend,
                                                                                           hms=_pause(
                                                                                               shiftend - shiftstart))
                if shiftlabel is not None:
                    staff['labels'][shiftday] = shiftlabel
                    if shiftlabel not in labels and len(labels) <= 16:
                        labels[shiftlabel] = label_classes[len(labels)]
                break
    return staff_list, labels


if __name__ == '__main__':
    print 'Kronos schedule tool'
    print '--------------------'
    print ''
    if len(sys.argv) > 2:
        week = week_parse[int(sys.argv[1]) - 1]
        username = sys.argv[2]
        if len(sys.argv) == 4:
            password = sys.argv[3]
        else:
            password = getpass('Please enter your Kronos password: ')
    else:
        weekno = ''
        print 'For which week shall we download the schedule?\n1 - Current Week\n2 - Next Week'
        while weekno not in ['1', '2']:
            weekno = raw_input('Please enter week number [1 or 2]: ')
        week = week_parse[int(weekno) - 1]
        print ''
        username = raw_input('Please enter your associate number: ')
        password = getpass('Please enter your Kronos password: ')
    print 'Trying to download schedule...'
    reqdone = False
    retry = 0
    sched = ''
    while not reqdone and retry < RETRIES:
        try:
            sched = get_schedule(username, password, week[0], week[6])
            reqdone = True
        except ConnectionError, e:
            print 'Server rejected the connection. Retrying...'
            if len(sys.argv) > 1 and sys.argv[1] == '-v':
                print e.message
            reqdone = False
            retry += 1
            sleep(1)
        except HTTPError, e:
            print 'The request failed with error ' + e.message
            retry = 6
            reqdone = False
    if not reqdone:
        print 'Fatal Error: Unable to retrieve schedule. Verify username / password.'
    else:
        sched, labels = parse_schedule(sched)
        html = template(schedule, datefrom=date_to_fr_ca(week[0]), dateto=date_to_fr_ca(week[6]), sched=sched,
                        labels=labels)
        html = html.encode('utf-8')
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            f.write(html)
            webbrowser.open('file://' + f.name)

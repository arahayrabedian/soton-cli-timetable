#!/usr/bin/env python

import argparse
import datetime
import json
from getpass import getpass

from display import tablify
from fetching import get_timetable_data
from fetching import get_session_cookie

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='University of Southampton '
                                                 'CLI Timetable')
    parser.add_argument('student_id',
                        metavar='student_id',
                        type=str,
                        help='Your student ID #, required to retrieve your '
                             'timetable from the timetable API')
    parser.add_argument('username',
                        metavar='isolutions_username',
                        type=str,
                        help='Your iSolutions username, required to log in to'
                             'the timetabling website - it\'s a hack, I know.')
    parser.add_argument('--password',
                        metavar='isolutions_password',
                        type=str,
                        help='Your iSolutions password, required to log in to '
                             'the timetabling website. You can choose to be '
                             'prompted (by skipping this switch/option), '
                             'this switch is useful if you want to alias and '
                             'avoid typing your password each time.\n\nBeware '
                             'that options entered here remain in your shell '
                             'history.')
    parser.add_argument('--nextweek',
                        action='store_true',
                        help='Use this switch to show next week\'s timetable')

    cli_args = parser.parse_args()

    password = cli_args.password or getpass(prompt='iSolutions Password:')

    cookie = get_session_cookie(cli_args.username, password)

    current_time = datetime.datetime.now()
    current_year, current_week = current_time.isocalendar()[:2]

    if cli_args.nextweek:
        current_week += 1

    # general hack - monday is day 1 of iso cal, 6 is saturday.
    week_monday = datetime.datetime.strptime(
        ' '.join((str(current_year), str(current_week), '1')), '%Y %W %w'
    )
    week_saturday = datetime.datetime.strptime(
        ' '.join((str(current_year), str(current_week), '6')), '%Y %W %w'
    )

    timetable_data = get_timetable_data(cookie,
                                        cli_args.student_id,
                                        int(week_monday.timestamp()),
                                        int(week_saturday.timestamp()))
    timetable_data = json.loads(timetable_data)

    # awesome, we have our data - now we need to display it.
    tablify(timetable_data)

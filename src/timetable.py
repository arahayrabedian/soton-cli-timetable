#!/usr/bin/env python

import argparse
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

    cli_args = parser.parse_args()

    password = cli_args.password or getpass(prompt='iSolutions Password:')

    cookie = get_session_cookie(cli_args.username, password)
    timetable_data = get_timetable_data(cookie,
                                        cli_args.student_id,
                                        1488153600,
                                        1488585600)
    timetable_data = json.loads(timetable_data)

    # awesome, we have our data - now we need to display it.
    tablify(timetable_data)

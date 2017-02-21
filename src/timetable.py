#!/usr/bin/env python

import argparse
import json
from getpass import getpass

import requests
from bs4 import BeautifulSoup

# we will follow many redirects for the login page:
TIMETABLE_PAGE = 'https://timetable.soton.ac.uk/'


def _get_validation(html):
    """
    We need to extract some stupid asp.net form validation stuff from the
    html on the login screen - these are:
    __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION
    :param html:
    :return:
    """
    interesting_attrs = {
        "__VIEWSTATE",
        "__VIEWSTATEGENERATOR",
        "__EVENTVALIDATION",
    }
    attribute_values = dict()
    bs = BeautifulSoup(html, "html.parser")
    for attribute in interesting_attrs:
        attribute_values[attribute] = bs.find(
            'input', id=attribute
        ).attrs['value']

    return attribute_values


def _get_magic_page_login_data(html):
    """
    So usually JS makes this step invisible, but apparently there's a "FU"
    factor to logging in... you POST from logon to the service you're going
    to some random looking information. beats me.
    :param html: the html provided by this silly page.
    :return: dictionary of elements you'll need to submit to your destination.
    """
    # looking for "names" of inputs: wa, wresult, wctx, but we'll do this
    # by finding the form's children, we don't care about specifics.
    bs = BeautifulSoup(html, "html.parser")

    das_form = bs.find('form')
    form_post_url = das_form.attrs['action']
    form_children = das_form.find_all('input')

    attribute_values = dict()
    for child in form_children:
        try:
            attribute_values[child.attrs['name']] = child.attrs['value']
        except KeyError:
            pass

    return form_post_url, attribute_values


def get_session_cookie(username, password):
    """
    Log in to the soton sign in page, and get us a cookie we can use to make
    further reqeusts to timetable API
    :param username: username to log in with
    :param password: that username's password
    :return: a requests.cookies.RequestsCookieJar object that can be used
    for further requests.
    """
    login_payload = {
        "ctl00$ContentPlaceHolder1$UsernameTextBox": username,
        "ctl00$ContentPlaceHolder1$PasswordTextBox": password,
        "ctl00$ContentPlaceHolder1$SubmitButton": "Logon",
        "__db": "14",  # apparently this is magically important.
                       # no db no login.
    }

    with requests.session() as conn:
        login_page = conn.get(TIMETABLE_PAGE)  # we will be forced here.

        # get stuff we need to throw back at the login page.
        validation_attributes = _get_validation(login_page.content)
        login_payload.update(validation_attributes)
        headers = {'Referer': login_page.url}

        login_response = conn.post(login_page.url,
                                   data=login_payload,
                                   headers=headers)

        # TODO: break here when a password is incorrect.

        # ok, southampton login is super weird... what sort of sorcery is this?
        # also, no consise way to describe, apologies on the long names.
        magic_post_url, magic_post_attributes = _get_magic_page_login_data(
            login_response.content
        )

        conn.post(
            magic_post_url,
            data=magic_post_attributes
        )

        # sweet - we should be fully logged in cookied up here. happy bappy.
        return conn.cookies


def get_timetable_data(cookie, student_id, start_ts, end_ts):
    api_url = "{host}api/Timetable/Student/{student_id}".format(
        host=TIMETABLE_PAGE,
        student_id=student_id,  # creative, i know.
    )
    api_args = {
        "start": start_ts,
        "end": end_ts,
        "isDraft": 'false'
    }

    response = requests.get(api_url, params=api_args, cookies=cookie)
    return response.text


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='University of Southampton'
                                                 ' CLI Timetable')
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
    print(json.dumps(json.loads(timetable_data), indent=2))

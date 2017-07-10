# STATE - DEPRECATED/BROKEN

This project was already fragile and it was broken with a new login screen ([see issue](https://github.com/arahayrabedian/soton-cli-timetable/issues/6)) - I decided not to fix it. It's also been pulled from `pypi`.

# University of Southampton CLI Timetable

Get your timetable from the comfort of your CLI/shell.

# Installation

~~`pip install soton-cli-timetable`~~

# Usage

`timetable [-h] [--password isolutions_password] [--nextweek] student_id isolutions_username`

e.g: `timetable 123455678 jj1j12 --password yourpass`

if you don't provide a `--password` option, you will be prompted instead.

if you want next week's timetable, use `--nextweek`, creative, I know.

# Limitations / Known Flaws / Bugs - BEWARE!

- DOES NOT HANDLE MULTI-HOUR SLOTS, THEY WILL APPEAR AS ONE HOUR
- WILL NOT HANDLE CLASHES - IT WILL ONLY SHOW ONE ITEM, SILENTLY.

# Screenshot
(please don't come to my classes)
![screenshot](https://raw.githubusercontent.com/arahayrabedian/soton-cli-timetable/master/screenshot.png)

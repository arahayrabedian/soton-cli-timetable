import datetime
import json
from terminaltables.ascii_table import AsciiTable


"""
Sample single lecture slot:
{
    "allDay": false,
    "className": "Lecture",
    "code": "COMP6237 L1 (s2)",
    "end": "2017-03-03T14:00:00",
    "id": "77472FBAF8C6931BB8FA1682E6088116",
    "isDraft": false,
    "lecturers": [
        "Hare, Jon",
        "Brede, Markus"
    ],
    "locations": [
        "07 / 3031 (L/R F2)"
    ],
    "pattern": "18-25, 30-33",
    "start": "2017-03-03T13:00:00",
    "title": "Data Mining"
},
"""

def _dict_to_table(lectures, wrap_tight=False):

    # parse date and add actual date objects - this makes manipulation easier.
    # also, simultaneously bucket lectures by days. we'll handle specific
    # slots later.

    # would have loved to use default dict, but all days should be present
    # for consistency and 'obvious' empty days.
    daily_lectures = {
        0: dict(),
        1: dict(),
        2: dict(),
        3: dict(),
        4: dict(),
    }

    date_format = "%Y-%m-%dT%H:%M:%S"
    for lecture in lectures:
        lecture['start_time'] = datetime.datetime.strptime(
            lecture['start'], date_format
        )
        lecture['end_time'] = datetime.datetime.strptime(
            lecture['end'], date_format
        )

        # TODO: figure out how to deal with clashes
        # add lecture to a list that becomes the columns
        daily_lectures[
            lecture['start_time'].weekday()
        ][
            lecture['start_time'].hour
        ] = lecture

    # once final, sort each bucket by start time
    # for day in daily_lectures.values():
    #     day.sort(key=lambda k: k['start_time'].hour)

    # now we have each day as a column. yay.


    # wrap_tight --> find min/max start for the weeks
    if wrap_tight:
        earliest_start = min([lecture['start_time'].hour for lecture in lectures])
        latest_end = max([lecture['end_time'].hour for lecture in lectures])
    else:
        earliest_start = 9
        latest_end = 18

    hours_to_display = latest_end - earliest_start

    # now we have it all set up, let's fill in each column of the table.

    display_data = []
    for day in range(5):
        current_day = []
        display_data.append(current_day)
        for hour in range(hours_to_display):
            # TODO: figure out how to deal with multi-hour lectures
            try:
                current_day.append(daily_lectures[day][hour + earliest_start]['title'])
            except:
                # no lecture here
                current_day.append("")

    # now format it correctly for table.
    display = [
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    ]

    for row in range(hours_to_display):
        display.append([
            display_data[0][row],
            display_data[1][row],
            display_data[2][row],
            display_data[3][row],
            display_data[4][row],
        ])

    return display


def tablify(data):
    table = AsciiTable(_dict_to_table(data))
    print(table.table)

from datetime import timedelta

import jdatetime


def persian_to_django_date(persian_date_str):
    if persian_date_str is None:
        return None
    # Split the date and time parts
    date_part, time_part = persian_date_str.split()

    # Parse the date and time parts
    year, month, day = map(int, date_part.split("/"))
    hour, minute = map(int, time_part.split(":"))

    # Create a jdatetime object
    persian_date = jdatetime.datetime(year, month, day, hour, minute)

    # Convert to Gregorian datetime
    gregorian_date = persian_date.togregorian()
    # fix time zone
    gregorian_date -= timedelta(hours=3, minutes=30)

    # Format the datetime object in Django's default datetime format
    django_date_str = gregorian_date.strftime("%Y-%m-%d %H:%M:%S")

    return django_date_str

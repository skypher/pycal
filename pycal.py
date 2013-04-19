from event_storage import *
import time

from datetime import datetime
from sys import argv

import redis


# TODO 'every X days'
def parse_appointment_date (s):
    target_time = None

    for pattern in ["%d", "%d %b", "%d %b %H:%M"]:
        try:
            target_time = datetime.strptime(s, pattern)
        except ValueError:
            continue
        break

    target_time = target_time.replace(year=datetime.today().year)

    if (target_time < datetime.today()):
        target_time = target_time.replace(year=datetime.today().year+1)

    return target_time

r = redis.StrictRedis()

if __name__ == "__main__":
    if (len(argv) == 1):
        #print "Next 3 appointments:"
        #map(print_appointment, get_appointments(r, 3))
        map(print_appointment, get_appointments(r))
        print "If no appointments, show help instead."
        print "Example: pycal ..."
    else:
        date = parse_appointment_date(argv[1])
        print_appointment(add_appointment(r, date, "test appointment"))


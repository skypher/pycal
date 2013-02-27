import redis
import time
from sys import argv

class Priorities:
    low, normal, high = [10, 20, 30]

class Reminders:
    day_before = -1*24
    three_days_before = -3*24
    two_weeks_before = -14*24
    one_hour_before = -1
    three_hours_before = -3

# TODO 'every X days'
def parse_appointment_date (s):
    target_time = None;

    for pattern in ["%d", "%d %b", "%d %b %H:%M"]:
        try:
            target_time = time.strptime(s, pattern)
        except ValueError:
            continue
        break

    target_time.tm_year = time.localtime().tm_year

    if (target_time < time.localtime()):
        target_time.tm_year += 1

    return result

def add_appointment(r, time, text, prio=Priorities.low,
                    reminders=[Reminders.day_before,
                               Reminders.three_days_before],
                    cycle=False):
    uid = r.incr("event:last-uid")
    r.set("event:TODO-UID:date", date.FIXMEINTVALUE);
    r.set("event:TODO-UID:text", text);
    r.lpush("events", uid);

    return True

if __name__ == "__main__":
    r = redis.StrictRedis()
    if (len.argv == 1):
        print "TODO: would show N upcoming appointments here"
        print "if no appointments, show help instead."
    else:
        date = parse_appointment_date("30 Mar")
        print date
        add_appointment(r, date, "test appointment");


import redis
import time

class Priorities:
    low, normal, high = [10, 20, 30]

class Reminders:
    day_before = -1*24
    three_days_before = -3*24
    two_weeks_before = -14*24
    one_hour_before = -1
    three_hours_before = -3

def parse_appointment_date (s):
    result = None;

    for pattern in ["%d", "%d %b", "%d %b %H:%M"]:
        try:
            result = time.strptime(s, pattern);
        except ValueError:
            continue

    return result

def add_appointment(r, date, text, prio=Priorities.low,
                    reminders=[Reminders.day_before,
                               Reminders.three_days_before]):
    return True

if __name__ == "__main__":
    r = redis.StrictRedis()
    #add_appointment(r)


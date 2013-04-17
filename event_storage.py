import redis
import time

from datetime import datetime

TAG_DELIMITER = '%%%'

class Priorities:
    low, normal, high = [10, 20, 30]

class Reminders:
    day_before = -1*24
    three_days_before = -3*24
    two_weeks_before = -14*24
    one_hour_before = -1
    three_hours_before = -3

class Appointment:
    def __init__(self, id, datetime, text,
                 priority=Priorities.low,
                 reminders=[Reminders.day_before,
                            Reminders.three_days_before],
                 tags=[],
                 cycle=False):
        self.id = id
        self.datetime = datetime
        self.text = text
        self.priority = priority
        self.reminders = reminders
        self.tags = tags
        self.cycle = cycle

def delete_appointments(r):
    i = 0
    for id in get_appointments(r, id_only=True):
        delete_appointment(r, id)
        i += 1
    return i

def delete_appointment(r, id):
    r.delete("event:%d:date" % id, "event:%d:text" % id)
    r.lrem("events", 0, id)

def get_appointment(r, id):
    # some stuff we don't support yet, e.g. Priorities
    date = r.get("event:%d:date" % id)
    date = datetime.fromtimestamp(int(float(date)))
    text = r.get("event:%d:text" % id)
    tags = r.get("event:%d:tags" % id).split(TAG_DELIMITER)
    if tags == ['']:
        tags = []
    return Appointment(id, date, text, tags=tags)

def get_appointments(r, limit=-1, id_only=False):
    events = r.lrange('events', 0, limit)

    if id_only is True:
        return map(int, events)
    return [get_appointment(r, int(event)) for event in events]

def get_appointments_for_month(r, month):
    apps = get_appointments(r)
    apps = filter((lambda app: app.datetime.month == month), apps)
    return apps

def print_appointment(app):
    print "%s: %s %s" % (app.datetime, app.text, app.tags)

def add_appointment(r, target_datetime, text, tags=[]):
    if (isinstance(target_datetime, basestring)):
        target_datetime = parse_appointment_date(target_datetime)

    uid = r.incr("event:last-uid")
    r.set("event:%d:date" % uid, (time.mktime(target_datetime.timetuple())))
    r.set("event:%d:text" % uid, text)
    r.set("event:%d:tags" % uid, TAG_DELIMITER.join(tags))
    r.lpush("events", uid)

    return uid


from flask import Flask, Markup, render_template, request, g
import jinja2
import flask_sijax

import os
import time
import operator

from event_storage import *
from datetime import datetime
import htmlCalendar

tags = []

class Tag:
    def __init__(self, name, icon=None):
        self.name = name
        self.icon_type, self.icon_data = icon.split(':')

    def __str__(self):
        return '%s,%s:' % (self.name, self.icon_type, self.icon_data)

    def register(self):
        tags.append(self)

def find_tag(name):
    for tag in tags:
        if tag.name == name:
            return tag
    else:
        return None

Tag('PORT ZERO', 'img:port-zero-fav.png').register()
Tag('Cloud', 'color:blue').register()
Tag('Michael', 'color:darkgreen').register()

app = Flask(__name__, static_folder='templates')
app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'templates/sijax_js/')
flask_sijax.Sijax(app)

@app.route('/')
def show_month_view():
    def sgn(x):
        if x > 1:
            return +1
        else:
            return -1

    def make_calendar(month_offset=0):
        cur_year = time.localtime().tm_year
        cur_mon = time.localtime().tm_mon
        # modular arithmetic with some minor adjustments
        effective_month = ((cur_mon + month_offset - 1) % 12) + 1
        effective_year = cur_year + ((cur_mon + month_offset - 1) // 12)

        cal = None
        if month_offset == 0:
            cal = htmlCalendar.MonthlyCalendar(effective_year, effective_month, cssClass='current')
        else:
            cal = htmlCalendar.MonthlyCalendar(effective_year, effective_month)

        for app in get_appointments_for_month(r, effective_month):
            cal.viewEvent(app.datetime.day, app.datetime.day, app.text,
                          [find_tag(name) for name in app.tags])

        cal.offset = 2 # week starts on Monday
        return cal

    prev_cals = [make_calendar(mo) for mo in range(-2,0)]
    cur_cal = make_calendar()
    next_cals = [make_calendar(mo) for mo in range(1,3)]

    prev_cals_html = reduce(operator.add, [cal.create() for cal in prev_cals])
    cur_cal_html = cur_cal.create()
    next_cals_html = reduce(operator.add, [cal.create() for cal in next_cals])

    merged_html = '<div class="previous_calendars">' + prev_cals_html + '</div>';
    merged_html += '<div class="current_calendars">' + cur_cal_html + '</div>';
    merged_html += '<div class="next_calendars">' + next_cals_html + '</div>';

    return render_template("cal.html",
                           cals_html=jinja2.Markup(merged_html),
                           events=get_appointments(r),
                           tags=tags)

@flask_sijax.route(app, '/add-event')
def add_event():
    def process_add_event(obj_response, values):
        print values
        date = map(int, values['date'].split('-'))
        add_appointment(r, datetime(date[0], date[1], date[2]), values['text'], values['tags'])

        obj_response.script("$('#dialog').dialog('close');")

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('process_add_event', process_add_event)
        return g.sijax.process_request()

    as_dialog = request.args.get('dialog')
    date = request.args.get('date').split('-')
    year, month, day = date

    return render_template("add-event.html", year=year, month=month,
                           day=day, tags=tags)

app.debug = True

r = redis.StrictRedis()

if __name__ == '__main__':
    app.run()


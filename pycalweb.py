from flask import Flask, Markup, render_template, request, g
import jinja2
import flask_sijax

import os
import time
import operator

from event_storage import *
import htmlCalendar

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
        offset_month = ((cur_mon + month_offset - 1) % 12) + 1
        offset_year = cur_year + ((cur_mon + month_offset - 1) // 12)

        cal = None
        if month_offset == 0:
            cal = htmlCalendar.MonthlyCalendar(offset_year, offset_month, cssClass='current')
        else:
            cal = htmlCalendar.MonthlyCalendar(offset_year, offset_month)

        cal.offset = 2
        return cal

    prev_cals = [make_calendar(mo) for mo in range(-2,0)]
    cur_cal = make_calendar()
    next_cals = [make_calendar(mo) for mo in range(1,3)]

    # test
    cur_cal.viewEvent(6, 8, "testev", "Test event")

    prev_cals_html = reduce(operator.add, [cal.create() for cal in prev_cals])
    cur_cal_html = cur_cal.create()
    next_cals_html = reduce(operator.add, [cal.create() for cal in next_cals])

    merged_html = '<div class="previous_calendars">' + prev_cals_html + '</div>';
    merged_html += '<div class="current_calendars">' + cur_cal_html + '</div>';
    merged_html += '<div class="next_calendars">' + next_cals_html + '</div>';

    global r
    events_html = ''
    for event in get_appointments(r):
        events_html += '<div class="event">%s</div>' % event.text

    return render_template("cal.html",
                           cals_html=jinja2.Markup(merged_html),
                           events_html=jinja2.Markup(events_html))

@flask_sijax.route(app, '/add-event')
def add_event():
    def process_add_event(obj_response, values):
        print values
        obj_response.script("$('#dialog').dialog('close');")

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('process_add_event', process_add_event)
        return g.sijax.process_request()

    action = request.args.get('action')
    if action == 'add':
        #js = 
        #return render_template('html-response.html', js=js)
        return '<script type="text/javascript">$("#dialog").close();'
    else:
        as_dialog = request.args.get('dialog')
        date = request.args.get('date').split('-')
        year, month, day = date
        return render_template("add-event.html", year=year, month=month, day=day)

app.debug = True

r = redis.StrictRedis()

if __name__ == '__main__':
    app.run()


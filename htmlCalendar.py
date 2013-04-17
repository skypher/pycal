"""
 +-------------------------------------------------------------------+
 |                  H T M L - C A L E N D A R   (v2.16)              |
 |                                                                   |
 | Copyright Gerd Tentler               www.gerd-tentler.de/tools    |
 | Created: May 27, 2003                Last modified: Feb. 12, 2012 |
 +-------------------------------------------------------------------+
 | This program may be used and hosted free of charge by anyone for  |
 | personal purpose as long as this copyright notice remains intact. |
 |                                                                   |
 | Obtain permission before selling the code for this program or     |
 | hosting this software on a commercial website or redistributing   |
 | this software over the Internet or in any other medium. In all    |
 | cases copyright must remain intact.                               |
 +-------------------------------------------------------------------+

 EXAMPLE #1:  myCal = calendar.MonthlyCalendar()
              print myCal.create()

 EXAMPLE #2:  myCal = calendar.MonthlyCalendar(2004, 12)
              print myCal.create()

 EXAMPLE #3:  myCal = calendar.MonthlyCalendar()
              myCal.year = 2004
              myCal.month = 12
              print myCal.create()

 Returns HTML code
=========================================================================================================
"""

import time
import math
import operator

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

cal_ID = 0

class MonthlyCalendar:
	"""creates a monthly calendar"""
	def __init__(self, year = None, month = None, week = None, cssClass = ''):
#========================================================================================================
# Configuration
#========================================================================================================
                self.cssClass = cssClass
		self.tFontFace = 'Arial, Helvetica' # title: font family (CSS-spec, e.g. "Arial, Helvetica")
		self.tFontSize = 14                 # title: font size (pixels)
		self.tFontColor = '#FFFFFF'         # title: font color
		self.tBGColor = '#304B90'           # title: background color

		self.hFontFace = 'Arial, Helvetica' # heading: font family (CSS-spec, e.g. "Arial, Helvetica")
		self.hFontSize = 12                 # heading: font size (pixels)
		self.hFontColor = '#FFFFFF'         # heading: font color
		self.hBGColor = '#304B90'           # heading: background color

		self.dFontFace = 'Arial, Helvetica' # days: font family (CSS-spec, e.g. "Arial, Helvetica")
		self.dFontSize = 14                 # days: font size (pixels)
		self.dFontColor = '#000000'         # days: font color
		self.dBGColor = '#FFFFFF'           # days: background color

		self.wFontFace = 'Arial, Helvetica' # weeks: font family (CSS-spec, e.g. "Arial, Helvetica")
		self.wFontSize = 12                 # weeks: font size (pixels)
		self.wFontColor = '#FFFFFF'         # weeks: font color
		self.wBGColor = '#304B90'           # weeks: background color

		self.saFontColor = '#0000D0'        # Saturdays: font color
		self.saBGColor = '#F6F6FF'          # Saturdays: background color

		self.suFontColor = '#D00000'        # Sundays: font color
		self.suBGColor = '#FFF0F0'          # Sundays: background color

		self.tdBorderColor = '#FF0000'      # today: border color

		self.borderColor = '#304B90'        # border color
		self.hilightColor = '#FFFF00'       # hilight color (works only in combination with link)

		self.link = ''                      # page to link to when day is clicked
		self.linkTarget = ''				# link target frame or window, e.g. parent.myFrame
		self.offset = 1                     # week start: 0 - 6 (0 = Saturday, 1 = Sunday, 2 = Monday ...)
		self.weekNumbers = 1                # view week numbers: 1 = yes, 0 = no

#--------------------------------------------------------------------------------------------------------
# You should change these variables only if you want to translate them into your language:
#--------------------------------------------------------------------------------------------------------
		# weekdays: must start with Saturday because January 1st of year 1 was a Saturday
		self.weekdays = ('Sa', 'So', 'Mo', 'Di', 'Mi', 'Do', 'Fr')

		# months: must start with January
		self.months = ('Januar', 'Februar', u'Maerz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember')

		# error messages
		self.error = ('Year must be 1 - 3999!', 'Month must be 1 - 12!')
#========================================================================================================

		if year is None and month is None:
			year = time.localtime().tm_year
			month = time.localtime().tm_mon
		elif year is None and month is not None: year = time.localtime().tm_year
		elif month is None: month = 1
		if week is None: week = 0;
		self.year = int(year)
		self.month = int(month)
		self.week = int(week)
		self.specDays = {}
		self.specDays2 = {}
		if self.linkTarget == '': self.linkTarget = 'document'

	__size = 0
	__mDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

	def set_styles(self):
		"""set calendar styles"""
		globals()['cal_ID'] += 1
		return ''

	def leap_year(self, year):
		"""check if year is a leap year"""
		return not (year % 4) and (year < 1582 or year % 100 or not (year % 400))

	def get_weekday(self, year, days):
		"""return weekday (0 - 6) of nth day in year"""
		a = days
		if year: a += (year - 1) * 365
		for i in range(1, year):
			if self.leap_year(i): a += 1
		if year > 1582 or (year == 1582 and days > 277): a -= 10
		if a: a = (a - self.offset) % 7
		elif self.offset: a += 7 - self.offset
		return a

	def get_week(self, year, days):
		"""return week number of nth day in year"""
		firstWDay = self.get_weekday(year, 0)
		if year == 1582 and days > 277: days -= 10

		return int(math.floor((days + firstWDay) / 7) + (firstWDay <= 3))

	def table_cell(self, content, cls = '', date = '', style = ''):
		"""return formatted table cell with content"""
		size = int(round(self.__size * 1.5))

                html = '<td'
                classes = [cls]
                final_content = ''

                if content != '&nbsp;': #and cls.lower().find('day') != -1:
			link = self.link
			eventClass = ''
			events = []
                        tags = []

                        final_content += '<ul class="tags">'
			if self.specDays.has_key(content):
				for v in self.specDays[content]:
					if v[0]: eventClass = v[0]
					if v[1]: events.append(v[1])
					if v[2]: link = v[2]
                                        if v[1]:
                                            tags = tags + v[1]
                                tags = list(frozenset(tags))
				html += ' title="' + ' &middot; '.join(events) + '"'
                                classes.append('event')
                                for tag in tags:
                                    if tag.icon_type == 'color':
                                        background = tag.icon_data
                                    elif tag.icon_type == 'img':
                                        background = "url('/templates/%s')" % tag.icon_data
                                    else:
                                        raise Exception("Tag icon type must be either 'color' or 'img'!")
                                    final_content += '<li title="%s" style="background:%s;"></li>' % (tag.name, background)
                                # TODO append tags to css classes
				#if eventClass:
                                #    classes.append(eventClass)

                        final_content += '</ul>'
                        final_content += '<div class="content">' + content + '</div>'
                        html += (' class="%s"' % reduce(operator.add, intersperse(classes, ' ')))
			if link:
				link += (link.find('?') != -1) and '&date=' + date or '?date=' + date
				html += ' onMouseOver="this.className=\'cssHilight' + str(globals()['cal_ID']) + '\'"'
				html += ' onMouseOut="this.className=\'' + cls + '\'"'
				html += ' onClick="' + self.linkTarget + '.location.href=\'' + link + '\'"'
		if style: html += ' style="' + style + '"'
		html += '>' + final_content + '</td>'
		return html

	def table_head(self, content):
		"""return formatted table head with content"""
		cols = self.weekNumbers and '8' or '7'
                html = '<thead>'
		html += '<tr><th colspan=' + cols + ' class="cssTitle' + str(globals()['cal_ID']) + '"><b>' + \
		 	content + '</b></th></tr><tr>'
		for i in range(len(self.weekdays)):
			ind = (i + self.offset) % 7
			wDay = self.weekdays[ind]
			html += self.table_cell(wDay)
		if self.weekNumbers: html += self.table_cell('KW')
		html += '</tr>'
                html += '</thead>'
		return html

	def viewEvent(self, start, end, title, tags=[]):
		"""add event to calendar"""
		if start > end: return
		if start < 1 or start > 31: return
		if end < 1 or end > 31: return
		while start <= end:
			if not self.specDays.has_key(str(start)): self.specDays[str(start)] = []
			self.specDays[str(start)].append((color, title, link))
			start += 1

	def viewEventEach(self, weekday, title, tags=[]):
		"""add event to calendar"""
		if weekday < 0 or weekday > 6: return
		if not self.specDays2.has_key(str(weekday)): self.specDays2[str(weekday)] = []
		self.specDays2[str(weekday)].append((title, tags))

	def create(self):
		"""create monthly calendar"""
		self.__size = (self.hFontSize > self.dFontSize) and self.hFontSize or self.dFontSize
		if self.wFontSize > self.__size: self.__size = self.wFontSize

		date = time.strftime('%Y-%m-%d', time.localtime())
		(curYear, curMonth, curDay) = [int(v) for v in date.split('-')]

		if self.year < 1 or self.year > 3999: html = '<b>' + self.error[0] + '</b>'
		elif self.month < 1 or self.month > 12: html = '<b>' + self.error[1] + '</b>'
		else:
			self.__mDays[1] = self.leap_year(self.year) and 29 or 28
			days = 0
			for i in range(self.month - 1): days += self.__mDays[i]

			start = self.get_weekday(self.year, days)
			stop = self.__mDays[self.month-1]

			html = self.set_styles()
			html += ('<table class="calendar %s"><tr>' % self.cssClass)
			title = self.months[self.month-1] + ' ' + str(self.year)
			html += self.table_head(title)
			daycount = 1

			if self.year == curYear and self.month == curMonth: inThisMonth = 1
			else: inThisMonth = 0

			if self.weekNumbers or self.week: weekNr = self.get_week(self.year, days)

			for i in range(self.__mDays[self.month-1] + 1):
				for j, v in self.specDays2.iteritems():
					if self.get_weekday(self.year, days + i) == int(j) - self.offset + 1:
						if not self.specDays.has_key(str(i)): self.specDays[str(i)] = []
						for v in self.specDays2[j]:
							self.specDays[str(i)].append(v)

			while daycount <= stop:
				if self.week and self.week != weekNr:
					daycount += 7 - (daycount == 1 and start or 0)
					weekNr += 1
					continue
				html += '<tr>'
				wdays = 0

				for i in range(len(self.weekdays)):
					ind = (i + self.offset) % 7
					if ind == 0: cls = 'Sa'
					elif ind == 1: cls = 'Su'
					else: cls = self.weekdays[i]

					style = ''
					date = "%4d-%02d-%02d" % (self.year, self.month, daycount)

					if (daycount == 1 and i < start) or daycount > stop: content = '&nbsp;'
					else:
						content = str(daycount)
                                                content += ('<a class="add-event" href="#" onclick="addEvent(%d,%d,%d);">+</a>' %
                                                            (self.year, self.month, daycount))
						if inThisMonth and daycount == curDay:
							style = 'padding:0px;border:3px solid ' + self.tdBorderColor + ';'
						elif self.year == 1582 and self.month == 10 and daycount == 4: daycount = 14
						daycount += 1
						wdays += 1

					html += self.table_cell(content, cls, date, style)

				if self.weekNumbers:
					if not weekNr:
						if self.year == 1: content = '&nbsp;'
						elif self.year == 1583: content = '51'
						else: content = str(self.get_week(self.year - 1, 365))
					elif self.month == 12 and weekNr >= 52 and wdays < 4: content = '1'
					else: content = str(weekNr)

					html += self.table_cell(content, 'week')
					weekNr += 1

				html += '</tr>'
			html += '</table>'
		return html

if __name__ == '__main__':
	print __doc__

# The MIT License (MIT)
# 
# Copyright (c) 2018 stanwood GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import calendar
import datetime
import dateutil.tz
import logging
import re


class AmazonTimeParser(object):
    DAY_TIME_MAPPER = {
        'MO': (8, 30),  # morning
        'AV': (13, 00),  # after noon
        'EV': (18, 00),  # evening
        'NI': (21, 00),  # night
    }

    @classmethod
    def to_time(cls, amazon_time):
        """
        Parses alexa time output string to mapped time.

        :param (str) amazon_time: Amazon string time. Possible choices: [MO, AV, EV, NI].

        :returns: Time tuple with hour as first element and minutes as second,
            otherwise None when amazon_time is not parsable.
        :rtype: tuple
        """
        time = None

        if not amazon_time:
            return time

        try:
            time = cls.DAY_TIME_MAPPER[amazon_time]
        except KeyError:
            pass

        try:
            time = map(int, amazon_time.split(':'))
        except (ValueError, AttributeError):
            pass

        return time


class AmazonDateParser(object):
    """Amazon build-in date format parser.

    Amazon Alexa API reference:
        https://developer.amazon.com/docs/custom-skills/slot-type-reference.html#date
    """

    WEEK_MAPPER = {'w{}'.format(nr): 'w0{}'.format(nr) for nr in xrange(10)}

    _DATE_PATTERNS = {
        # "today", "tomorrow", "november twenty-fifth": 2015-11-25
        '^\d{4}-\d{2}-\d{2}$': ('%Y-%m-%d', 'normal'),
        # "this week", "next week": 2015-W48
        '^\d{4}-W\d{1,2}$': ('%Y-W%U-%w', 'week'),
        # "this weekend": 2015-W48-WE
        '^\d{4}-W\d{1,2}-WE$': ('%Y-W%U-WE-%w', 'weekend'),
        # "this month": 2015-11
        '^\d{4}-\d{2}$': ('%Y-%m', 'month'),
        # "next year": 2016
        '^\d{4}$': ('%Y', 'year'),
    }

    @classmethod
    def to_date(cls, amazon_date):
        """
        Parses alexa date output string to mapped time.

        :param (str) amazon_date: Amazon date string.

        :returns: Datetime with parsed date and date type. Otherwise (None, None) if date is not parsable.
        :rtype: tuple

        .. note::
            Possible date types:
                * normal
                * week
                * weekend
                * month
                * year
        """
        amazon_date = re.sub('X$', '0', amazon_date)

        for re_pattern, format_pattern_info in list(cls._DATE_PATTERNS.items()):
            format_pattern, date_type = format_pattern_info

            if re.match(re_pattern, amazon_date):

                if '%U' in format_pattern:
                    amazon_date += '-0'
                    amazon_date = reduce(lambda a, kv: a.replace(*kv), cls.WEEK_MAPPER.iteritems(), amazon_date)

                date = datetime.datetime.strptime(amazon_date, format_pattern)
                date = date.replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))
                logging.debug(date_type)
                logging.debug(date)

                return date, date_type

        return None, None

    @classmethod
    def create_periods(cls, amazon_date, timezone=dateutil.tz.gettz('Europe/Berlin')):
        date, date_type = cls.to_date(amazon_date)
        today = datetime.datetime.now().replace(tzinfo=timezone)

        if date_type == 'weekend':
            start = date - datetime.timedelta(days=1)
            start = today if start < today else start
            end = date

        elif date_type == 'week':
            start = date - datetime.timedelta(days=6)
            end = date

        elif date_type == 'month':
            start = date
            month = calendar.monthrange(date.year, date.month)
            end = start.replace(day=month[1])

        elif date_type == 'year':
            start = date
            end = start.replace(month=12, day=31)

        elif date_type == 'normal':
            start = date
            end = start + datetime.timedelta(hours=4)

        else:
            start = end = None

        return start, end

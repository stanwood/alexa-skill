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
import datetime

import dateutil.tz

from alexa_skill import dates as alexa_dates


def test_amazon_dates_normal_day():
    date_value = '2017-12-22'  # "today", "tomorrow", "november twenty-fifth": 2015-11-25
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2017, 12, 22).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))
    assert date_type == 'normal'


def test_amazon_dates_weekend():
    date_value = '2017-W51-WE'   # "this weekend": 2015-W48-WE
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2017, 12, 17).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_dates_week():
    date_value = '2017-W51'  # "this week", "next week": 2015-W48
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2017, 12, 17).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_dates_english_week():
    date_value = '2018-W01'  # English version is returning  W\d{2}
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2018, 1, 7).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_dates_german_week():
    date_value = '2018-W1'  # German version is returning W\d{1-2}
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2018, 1, 7).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_dates_month():
    date_value = '2018-01'  # "this month": 2015-11
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2018, 1, 1, 0, 0).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_dates_year():
    date_value = '2018'  # "next year": 2016
    result, date_type = alexa_dates.AmazonDateParser.to_date(date_value)

    assert result == datetime.datetime(2018, 1, 1, 0, 0).replace(tzinfo=dateutil.tz.gettz('Europe/Berlin'))


def test_amazon_time():
    date_value = '11:30'
    hour, minute = alexa_dates.AmazonTimeParser.to_time(date_value)

    assert hour == 11
    assert minute == 30


def test_amazon_time_morning():
    date_value = 'MO'
    hour, minute = alexa_dates.AmazonTimeParser.to_time(date_value)

    assert hour == 8
    assert minute == 30


def test_amazon_time_evening():
    date_value = 'EV'
    hour, minute = alexa_dates.AmazonTimeParser.to_time(date_value)

    assert hour == 18
    assert minute == 0


def test_amazon_time_none():
    date_value = None
    time = alexa_dates.AmazonTimeParser.to_time(date_value)

    assert time is None


def test_amazon_time_parsing_error():
    date_value = '11:dwa'
    time = alexa_dates.AmazonTimeParser.to_time(date_value)

    assert time is None

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
import logging

import falcon

import alexa_skill
from alexa_skill.intents import BaseIntents
from alexa_skill.intents import BuildInIntents
from alexa_skill import dates


class ExampleIntents(BaseIntents):
    @property
    def mapper(self):
        return {
            'EXAMPLE.hello': self.hello,
            'EXAMPLE.date_intent': self.date_intent,
        }

    def hello(self):
        return self.response('Hello. Nice to meet you.'), True

    def date_intent(self, slots=None):

        date, date_type = dates.AmazonDateParser.to_date(slots['dateslot']['value'])

        text = "Your date is <say-as interpret-as='date'>{}</say-as> and it is a {}".format(
            date.strftime('%Y%m%d'),
            date_type
        )

        return self.response(text), True


buildin_intents = BuildInIntents(
    help_message='Say "HI" to us',
    not_handled_message="Sorry, I don't understand you. Could you repeat?",
    stop_message='stop',
    cancel_message='cancel'
)


class Fulfiller(object):
    def on_post(self, req, resp):
        get_response = alexa_skill.Processor(
            req.media,
            buildin_intents,
            'Welcome to Alexa skill bot',
            'Good bye',
            ExampleIntents(),
        )
        json_response, handled = get_response()

        logging.info('Response was handled by system: {}'.format(handled))

        resp.media = json_response


app = falcon.API(media_type=falcon.MEDIA_JSON)
app.add_route('/v1/alexa/fulfiller', Fulfiller())

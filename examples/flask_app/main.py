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

from flask import Flask, request, jsonify

import alexa_skill
from alexa_skill.intents import BaseIntents
from alexa_skill.intents import BuildInIntents


app = Flask(__name__)

buildin_intents = BuildInIntents(
    help_message='Say "HI" to us',
    not_handled_message="Sorry, I don't understand you. Could you repeat?",
    stop_message='stop',
    cancel_message='cancel'
)


class ExampleIntents(BaseIntents):
    @property
    def mapper(self):
        return {
            'EXAMPLE.hello': self.hello,
        }

    def hello(self):
        return self.response('Hello. Nice to meet you.'), True


@app.route("/v1/alexa/fulfiller", methods=['POST'])
def fulfiller():
    get_response = alexa_skill.Processor(
        request.json,
        buildin_intents,
        'Welcome to Alexa skill bot',
        'Good bye',
        ExampleIntents(),
    )
    json_response, handled = get_response()

    logging.info('Response was handled by system: {}'.format(handled))

    return jsonify(json_response)

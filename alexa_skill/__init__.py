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

from alexa_skill import messages


class Processor(object):
    def __init__(self, request_body, buildin_intents, launch_message, session_end_message, *intents):
        """
        Creates instance of Alexa Processor which handles Alexa request and creates a response to it.

        :param (dict) request_body: Alexa request body which was send to fulfiller webhook.
        :param (intents.buildins.Alexa) buildin_intents: Instance of intents class which handles Alexa buildin intents
        :param (str) launch_message: Welcoming intent which will be fired on start for all users
        :param (str) session_end_message: Session end message which will be fired at the end of session.
        :param (list) *intents: List of additional intent classes which will handle user responses.

        Note:
            Intents classes should inherit from alexa_skill.intents.Base.
        """
        self.request_body = request_body
        self.launch_message = launch_message
        self.session_end_message = session_end_message
        self.buildin_intents = buildin_intents
        self.intents_mapper = {}

        map(self.intents_mapper.update, [intent.mapper for intent in intents])

    def __call__(self):
        request_types = {
            'IntentRequest': self.intent_request,
            'LaunchRequest': self.launch_request,
            'SessionEndedRequest': self.session_end_request,
        }
        return request_types[self.request_type]()

    @property
    def locale(self):
        """
        Used for setting i18n internationalization strings
        """
        return self.request_body['request']['locale']

    @property
    def slots(self):
        """
        Alexa slots which are defined in Alexa console.

        API Reference:
            https://developer.amazon.com/docs/custom-skills/slot-type-reference.html

        :rtype: dict
        """
        try:
            return self.request_body['request']['intent']['slots']
        except KeyError:
            return {}

    @property
    def intent_name(self):
        try:
            return self.request_body['request']['intent']['name']
        except LookupError:
            return None

    @property
    def request_type(self):
        return self.request_body['request']['type']

    @property
    def session_hash(self):
        """
        Return session hash of a user.
        """
        return self.request_body['session']['sessionId']

    @property
    def session_attributes(self):
        return self.request_body['session'].get('attributes')

    def session_end_request(self):
        """
        Returns a list with:
            0: message for user
            1: bool: True when alexa request was handled by Backend
        """

        message = messages.create_response(self.session_end_message, should_end_session=True)

        return message, True

    def launch_request(self):
        """
        Returns a list with:
            0: message for user
            1: bool: True when alexa request was handled by Backend
        """

        message = messages.create_response(self.launch_message, should_end_session=False)
        return message, True

    def intent_request(self):
        """
        Returns a list with:
            0: message for user
            1: bool: True when alexa request was handled by Backend
            2: bool: if session should be ended
        """

        if self.intent_name and self.intent_name.startswith('AMAZON'):
            message, handled = self.buildin_intents.mapper[self.intent_name]()
        else:
            try:
                kwargs = {'slots': self.slots} if self.slots else {}

                message, handled = self.intents_mapper[self.intent_name](**kwargs)
            except (ValueError, KeyError):
                logging.error('Intent name: {} not handled'.format(self.intent_name))
                message, handled = self.buildin_intents.mapper['NotHandled']()

        return message, handled

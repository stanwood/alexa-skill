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
from alexa_skill.intents.base import BaseIntents


class BuildInIntents(BaseIntents):
    """
    Buildin intents class which is handling all standard intents which are sent from Alexa.
    """

    def __init__(self, help_message, not_handled_message, stop_message='stop', cancel_message='cancel'):
        self.help_message = help_message
        self.not_handled_message = not_handled_message
        self.stop_message = stop_message
        self.cancel_message = cancel_message

    @property
    def mapper(self):
        return {
            'AMAZON.CancelIntent': self.cancel,
            'AMAZON.StopIntent': self.stop,
            'AMAZON.HelpIntent': self.help,
            'NotHandled': self.not_handled,
        }

    def cancel(self):
        """
        Handles build-in Alexa cancel intent.
        This method should end user session if no transactional action is made, otherwise it should end action.

        :returns: [Alexa voice message string, should end session bool]
        :rtype: list
        """

        response = self.response(self.cancel_message, should_end_session=True)

        return response, True

    def stop(self):
        """
        Handles build-in Alexa stop intent.

        :returns: [Alexa voice message string, should end session bool]
        :rtype: list
        """

        response = self.response(self.stop_message, should_end_session=True)

        return response, True

    def help(self):
        """
        Handles build-in Alexa help intent.

        :returns: [Alexa voice message string, should end session bool]
        :rtype: list
        """
        response = self.response(self.help_message, should_end_session=True)

        return response, True

    def not_handled(self):
        """
        Returns not handled message.

        :returns: [Alexa voice message string, should end session bool]
        """
        response = self.response(self.not_handled_message, should_end_session=False)
        return response, False

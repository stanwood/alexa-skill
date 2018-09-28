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
from alexa_skill import messages


def test_speech_output_ssml():
    test_text = 'Test text'

    result = messages.speech_output(test_text)

    assert result['type'] == 'SSML'
    assert result['ssml'] == '<speak>{}</speak>'.format(test_text)
    assert 'text' not in result


def test_speech_output_plain_text():
    test_text = 'Test text'
    speech_type = 'PlainText'

    result = messages.speech_output(test_text, speech_type=speech_type)

    assert result['type'] == speech_type
    assert result['text'] == test_text
    assert 'ssml' not in result


def test_cards():
    test_text = 'Test text'
    test_title = 'My app'

    result = messages.cards(test_title, test_text)

    assert result['type'] == 'Simple'
    assert result['title'] == test_title
    assert result['content'] == test_text


def test_reprompt_plain_text_default():
    test_text = 'Test text'

    result = messages.reprompt(test_text)

    assert result['outputSpeech']['text'] == test_text
    assert result['outputSpeech']['type'] == 'PlainText'


def test_reprompt_ssml():
    test_text = 'Test text'
    speech_type = 'SSML'

    result = messages.reprompt(test_text, speech_type=speech_type)

    assert result['outputSpeech']['ssml'] == '<speak>{}</speak>'.format(test_text)
    assert result['outputSpeech']['type'] == speech_type


def test_confirm_slots_directives():
    intent_name = 'intent_name'
    slots = {
        intent_name: {
            'name': intent_name,
            'confirmationStatus': 'NONE',
            'slots': {
                intent_name: {
                    'name': intent_name,
                    'value': 'intent_value',
                    'confirmationStatus': 'NONE'
              }
            }
        }
    }

    result = messages.confirm_slots_directives(slots)

    assert result[0]['type'] == 'Dialog.ConfirmSlot'
    assert result[0]['slotToConfirm'] == intent_name
    assert result[0]['updatedIntent'] == slots[intent_name]

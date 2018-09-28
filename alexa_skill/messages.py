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


def speech_output(text, speech_type='SSML'):
    """
    This function is used for setting both the outputSpeech and the reprompt properties.

    :param (str) text: Text which will be returned to the user.
    :param (str) speech_type: Type in which text is formatted. Choices: [SSML, PlainText]. Default: SSML
    :return: Alexa parsable dictionary.
    :rtype: dict

    Alexa API Reference:
        https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#outputspeech-object
    """
    if speech_type == 'SSML':
        return {
            'type': 'SSML',
            'ssml': '<speak>' + text + '</speak>',
        }
    else:
        return {
            'type': 'PlainText',
            'text': text,
        }


def cards(title, text, card_type="Simple", image=None):
    """
    Returns alexa cards

    :param str title: A string containing the title of the card.
    :param str text: A string containing the text content for a Standard card
        (not applicable for cards of type Simple)
    :param str card_type: A string describing the type of card to render. Valid types are:
        * "Simple": A card that contains a title and plain text content.
        * "Standard": A card that contains a title, text content, and an image to display.
    :param dict image: An image object that specifies the URLs for the image to display on a Standard card.
        Only applicable for Standard cards.
        You can provide two URLs, for use on different sized screens.
        * smallImageUrl
        * largeImageUrl
    :return: Dictionary with cards details
    :rtype: dict

    Alexa API Reference:
        https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#card-object

    """

    cards = {
        "type": card_type,
        "title": title,
    }

    if card_type == "Standard":
        cards["text"] = text
    else:
        cards["content"] = text

    if image:
        cards['image'] = image

    return cards


def reprompt(text, speech_type='PlainText'):
    """
    This object can only be included when sending a response to a [CanFulfillIntentRequest, LaunchRequest,
    IntentRequest, or InputHandlerEvent]

    :param (str) text: Text which will be returned to the user.
    :param (str) speech_type: Type in which text is formatted. Choices: [SSML, PlainText]. Default: SSML
    :return: Dictionary with output speech
    :rtype: dict

    Alexa API Reference:
        https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#reprompt-object
    """
    return {
        "outputSpeech": speech_output(text, speech_type=speech_type)
    }


def confirm_slots_directives(slots):
    """Used to ask user for missing slots.

    When confirm_slots is used, Alexa respond to a end user with message specified in `outputSpeech` element
    and expects the value for specified slots with the same intent as was detect in previous message.

    Alexa API Reference:
        https://developer.amazon.com/docs/custom-skills/dialog-interface-reference.html#confirmslot
    """
    message = [
        {
            "type": "Dialog.ConfirmSlot",
            "slotToConfirm": slot,
            "updatedIntent": updated_intent
        }
        for slot, updated_intent in slots.iteritems()
    ]
    return message


def create_response(
    text, card_title='', should_end_session=True, reprompt=None, confirm_slots=False, speech_type='SSML'
):
    """
    Creates response for Alexa skill with answer for user intent.

    :param (str) text: Text which should he responded to a user. Not required. Default: ''
    :param (str) card_title: Tile used in alexa cards
    :param (bool) should_end_session: Defines whether session should be close or not
                                      (Mike should listen for next user response or should close connection).
    :param (str) reprompt: Defines reprompt output speech text. Default: will be no reprompt.
    :param (dict) confirm_slots: Dict of slot name which require confirmation as key and updated intent dict as value.
    :param (str) speech_type: Defines type of speech which should be returned. Choices: SSML or PlainText.

    :return: Dict with Alexa response format.

    Alexa API Reference:
        https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format
    """
    message = {
        "version": "1.0",
        "response": {
            "outputSpeech": speech_output(text, speech_type=speech_type),
            "card": cards(card_title, text),
            "shouldEndSession": should_end_session,
        }
    }

    if reprompt:
        message['response']['reprompt'] = reprompt

    if confirm_slots:
        message['response']['directives'] = confirm_slots_directives(confirm_slots)

    return message

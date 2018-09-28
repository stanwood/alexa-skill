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
import pytest

import main


@pytest.fixture
def client():
    return main.app.test_client()


@pytest.fixture
def alexa_request_body():
    return {
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.[unique-value-here]",
                "application": {
                    "applicationId": "amzn1.ask.skill.[unique-value-here]"
                },
                "attributes": {
                    "key": "string value"
                },
                "user": {
                    "userId": "amzn1.ask.account.[unique-value-here]",
                    "accessToken": "Atza|AAAAAAAA...",
                    "permissions": {
                        "consentToken": "ZZZZZZZ..."
                    }
                }
            },
            "context": {
                "System": {
                    "device": {
                        "deviceId": "string",
                        "supportedInterfaces": {
                            "AudioPlayer": {}
                        }
                    },
                    "application": {
                        "applicationId": "amzn1.ask.skill.[unique-value-here]"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.[unique-value-here]",
                        "accessToken": "Atza|AAAAAAAA...",
                        "permissions": {
                            "consentToken": "ZZZZZZZ..."
                        }
                    },
                    "apiEndpoint": "https://api.amazonalexa.com",
                    "apiAccessToken": "AxThk..."
                },
                "AudioPlayer": {
                    "playerActivity": "PLAYING",
                    "token": "audioplayer-token",
                    "offsetInMilliseconds": 0
                }
            },
            "request": {
                "type": "LaunchRequest"
            }
        }


def test_post_launch_request_flask(client, alexa_request_body):
    response = client.post('/v1/alexa/fulfiller', json=alexa_request_body)

    assert response.status_code == 200
    assert response.json['response']['outputSpeech']['ssml'] == '<speak>Welcome to Alexa skill bot</speak>'
    assert response.json['response']['shouldEndSession'] is False


def test_post_intent_request_flask(client, alexa_request_body):
    request_body = alexa_request_body.copy()
    request_body['request'] = {
        'type': 'IntentRequest',
        'intent': {
            'name': 'EXAMPLE.hello',
        }
    }

    response = client.post('/v1/alexa/fulfiller', json=request_body)

    assert response.status_code == 200
    assert response.json['response']['outputSpeech']['ssml'] == '<speak>Hello. Nice to meet you.</speak>'
    assert response.json['response']['shouldEndSession'] is True


def test_not_handled_intent_request_flask(client, alexa_request_body):
    request_body = alexa_request_body.copy()
    request_body['request'] = {
        'type': 'IntentRequest',
        'intent': {
            'name': 'EXAMPLE.not_handled',
        }
    }

    response = client.post('/v1/alexa/fulfiller', json=request_body)

    assert response.status_code == 200
    assert response.json['response']['outputSpeech']['ssml'] == (
        "<speak>Sorry, I don't understand you. Could you repeat?</speak>"
    )
    assert response.json['response']['shouldEndSession'] is False

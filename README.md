# alexa-skill

[alexa-skill](https://github.com/stanwood/) is flexible, easy to use and extend package for creating Alexa skill applications.

This package is based on [alexa documentation](https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html).


## Installing

Install and update using pip:

```bash
pip install -U alexa-skill
```

## Examples

Define intent class

```python
from alexa_skill.intents import BaseIntents


class ExampleIntents(BaseIntents):
    @property
    def mapper(self):
        return {
            'EXAMPLE.hello': self.hello,
        }

    def hello(self):
        return self.response('Hello. Nice to meet you.'), True
```

Define intent class with slots

```python
from alexa_skill import dates
from alexa_skill.intents import BaseIntents


class DateIntents(BaseIntents):
    @property
    def mapper(self):
        return {
            'EXAMPLE.date_intent': self.date_intent,
        }

    def date_intent(self, slots):

        date, date_type = dates.AmazonDateParser.to_date(slots['dateslot']['value'])

        text = "Your date is <say-as interpret-as='date'>{}</say-as> and it is a {}".format(
            date.strftime('%Y%m%d'),
            date_type
        )

        return self.response(text), True

```

Define buildin intents

```python
from alexa_skill.intents import BuildInIntents


buildin_intents = BuildInIntents(
    help_message='Say "HI" to us',
    not_handled_message="Sorry, I don't understand you. Could you repeat?",
    stop_message='stop',
    cancel_message='cancel'
)
```

### [Falcon](examples/falcon_app/main.py)

Initiate intents in fulfiller webhook for Alexa

```python
import logging

import alexa_skill
import falcon


class Fulfiller(object):

    def on_post(self, req, resp):
        get_response = alexa_skill.Processor(
            req.media,
            buildin_intents,
            'Welcome to Alexa skill bot',
            'Good bye',
            ExampleIntents(),  # Insert created Intents as arguments
            DateIntents(),
        )
        json_response, handled = get_response()

        logging.info('Response was handled by system: {}'.format(handled))

        resp.media = json_response
        
app = falcon.API(media_type=falcon.MEDIA_JSON)
app.add_route('/v1/alexa/fulfiller', Fulfiller())
```

### [Flask](examples/flask_app/main.py)

```python
import logging

import alexa_skill
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/v1/alexa/fulfiller", methods=['POST'])
def fulfiller():
    get_response = alexa_skill.Processor(
        request.json,
        buildin_intents,
        'Welcome to Alexa skill bot',
        'Good bye',
        ExampleIntents(),
        DateIntents(),
    )
    json_response, handled = get_response()

    logging.info('Response was handled by system: {}'.format(handled))

    return jsonify(json_response)
```

## Documentation

Auto generate documentation

```bash

cd docs/

sphinx-apidoc -o ./source/_modules/ ../alexa_skill/

make html
```
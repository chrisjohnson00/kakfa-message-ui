# kakfa-message-ui
A simple UI to send messages to Kafka topics

## Run locally

Export the path to your in/out dir, then run the app

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
    
## Running tests

Write some first, then...

    python -m pytest

PyPi Dependency updates

    pip install --upgrade pip
    pip install --upgrade kafka-python Flask gunicorn
    pip freeze > requirements.txt
    sed -i '/pkg_resources/d' requirements.txt

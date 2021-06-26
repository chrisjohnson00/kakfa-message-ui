import os
from kafka import KafkaProducer
from json import dumps
from flask import (
    Blueprint, render_template, current_app as app, request
)

bp = Blueprint('topics', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    json_str = '''
{
  "py/object":"kme.kme.KMEMessage",
  "message":{
    "name":"nfs2",
    "mac_address":"b8:ca:3a:5d:28:b8",
    "ip":"192.168.1.132",
    "port":"22"
  },
  "topic":"wakeup-computer"
}
'''
    # @TODO pull `topics` from a yaml file in the environment, injectable at deploy time via a config map
    topics = [
        {'name': 'wakeup-computer', 'message': json_str}, {'name': 'nas-backup', 'message': ''}
    ]
    if request.method == 'POST':
        app.logger.info("Post on / received!")
        app.logger.info(f"topic: {request.form['topic']}")
        app.logger.info(f"message: {request.form['message']}")
        send_message(request.form['message'], request.form['topic'])
        return render_template('topics/list.html', topics=topics)
    else:
        return render_template('topics/list.html', topics=topics)


def send_message(message, kafka_topic):
    # send the message to kafka, if configured
    kafka_server = os.environ.get('KAFKA_BOOSTRAP_SERVER')
    if kafka_server and kafka_topic:
        producer = KafkaProducer(bootstrap_servers=[kafka_server],
                                 acks=1,
                                 api_version_auto_timeout_ms=10000,
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))

        future = producer.send(topic=kafka_topic, value=message)
        future.get(timeout=60)
        app.logger.info("Sent message {} to {}".format(message, kafka_topic))
    else:
        app.logger.warning("KAFKA_BOOSTRAP_SERVER was not found in configs, no messages will be sent")

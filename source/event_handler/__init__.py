import json
import sys
import traceback
from flask import Config
import pika
from .configuration import configuration
from .handle_event import send_mail as send_mail_


class EventHandler(object):

    def __init__(self):
        self.config = Config(__name__)


    def send_mail(self,
            recipients,
            subject,
            message):
        smtp_server = self.config["EMIS_SMTP_SERVER"]
        smtp_port = self.config["EMIS_SMTP_PORT"]
        smtp_sender = self.config["EMIS_SMTP_SENDER"]

        send_mail_(
            smtp_server, smtp_port, smtp_sender,
            recipients, subject, message)


    def critical_notify(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:
            body = body.decode("utf-8")
            data = json.loads(body)

        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc(exception)));
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def admin_notify(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:
            body = body.decode("utf-8")
            data = json.loads(body)

        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc(exception)));
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        self.credentials = pika.PlainCredentials(
            self.config["EMIS_RABBITMQ_DEFAULT_USER"],
            self.config["EMIS_RABBITMQ_DEFAULT_PASS"]
        )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=self.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
            credentials=self.credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
        ))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="alerts",
            type="topic",
            auto_delete=False)

        self.channel.queue_declare(
            queue="critical",
            auto_delete=False)
        self.channel.queue_bind(
            queue="critical",
            exchange="alerts",
            routing_key="critical.*")

        self.channel.queue_declare(
            queue="admin",
            auto_delete=False)
        self.channel.queue_bind(
            queue="admin",
            exchange="alerts",
            routing_key="*.rate_limit")

        self.channel.basic_consume(
            self.critical_notify,
            queue="critical",
            no_ack=False,
            consumer_tag="critical")
        self.channel.basic_consume(
            self.admin_notify,
            queue="admin",
            no_ack=False,
            consumer_tag="admin")

        try:
            sys.stdout.write("Start consuming...\n")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...\n")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = EventHandler()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app

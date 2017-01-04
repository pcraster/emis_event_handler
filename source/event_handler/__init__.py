import json
import sys
import traceback
from flask import Config
import pika
from .configuration import configuration
from .handle_event import log, send_mail


class EventHandler(object):

    def __init__(self):
        self.config = Config(__name__)


    def logs_uri(self,
            route):
        return "http://{}:{}/{}".format(
            self.config["EMIS_LOG_HOST"],
            self.config["EMIS_LOG_PORT"],
            route)


    def send_mail_(self,
            recipients,
            subject,
            message):
        smtp_server = self.config["EMIS_SMTP_SERVER"]
        smtp_port = self.config["EMIS_SMTP_PORT"]
        smtp_sender = self.config["EMIS_SMTP_SENDER"]

        send_mail(
            smtp_server, smtp_port, smtp_sender,
            recipients, subject, message)


    def default_notify(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:
            body = body.decode("utf-8")
            data = json.loads(body)
            uri = self.logs_uri("logs")
            timestamp = data["timestamp"]
            priority = data["priority"]
            severity = data["severity"]
            message = data["message"]

            log(uri, timestamp, priority, severity, message)

            sys.stdout.write("{}: {}, {}, {}\n".format(timestamp, priority, severity, message))
            sys.stdout.flush()

        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc(exception)));
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    ### def critical_notify(self,
    ###         channel,
    ###         method_frame,
    ###         header_frame,
    ###         body):
    ###     sys.stdout.write("received message: {}\n".format(body))
    ###     sys.stdout.flush()

    ###     try:
    ###         body = body.decode("utf-8")
    ###         data = json.loads(body)

    ###     except Exception as exception:

    ###         sys.stderr.write("{}\n".format(traceback.format_exc(exception)));
    ###         sys.stderr.flush()


    ###     channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    ### def admin_notify(self,
    ###         channel,
    ###         method_frame,
    ###         header_frame,
    ###         body):
    ###     sys.stdout.write("received message: {}\n".format(body))
    ###     sys.stdout.flush()

    ###     try:
    ###         body = body.decode("utf-8")
    ###         data = json.loads(body)

    ###     except Exception as exception:

    ###         sys.stderr.write("{}\n".format(traceback.format_exc(exception)));
    ###         sys.stderr.flush()


    ###     channel.basic_ack(delivery_tag=method_frame.delivery_tag)


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

        # pattern:
        # <priority>.<severity>
        # <low | high>.<critical | non_critical>
        # - All events are sent to the log service.
        # - Some events are handled special:
        #    - high.critical -> send e-mail to administrator

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="alerts",
            type="topic",
            auto_delete=False)

        self.channel.queue_declare(
            queue="default",
            auto_delete=False)
        self.channel.queue_bind(
            queue="default",
            exchange="alerts",
            routing_key="*.*")
        self.channel.basic_consume(
            self.default_notify,
            queue="default",
            no_ack=False,
            consumer_tag="default")

        # self.channel.queue_declare(
        #     queue="critical",
        #     auto_delete=False)
        # self.channel.queue_bind(
        #     queue="critical",
        #     exchange="alerts",
        #     routing_key="critical.*")

        # self.channel.queue_declare(
        #     queue="admin",
        #     auto_delete=False)
        # self.channel.queue_bind(
        #     queue="admin",
        #     exchange="alerts",
        #     routing_key="*.rate_limit")

        # self.channel.basic_consume(
        #     self.critical_notify,
        #     queue="critical",
        #     no_ack=False,
        #     consumer_tag="critical")
        # self.channel.basic_consume(
        #     self.admin_notify,
        #     queue="admin",
        #     no_ack=False,
        #     consumer_tag="admin")

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

import os


class Configuration:

    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")

    EMIS_SMTP_SERVER = os.environ.get("EMIS_SMTP_SERVER")
    EMIS_SMTP_PORT = os.environ.get("EMIS_SMTP_PORT")
    EMIS_SMTP_SENDER = os.environ.get("EMIS_SMTP_SENDER")

    EMIS_LOG_HOST = "log"


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    EMIS_LOG_PORT = 5000


class TestingConfiguration(Configuration):

    EMIS_LOG_PORT = 5000


class ProductionConfiguration(Configuration):

    EMIS_LOG_PORT = 3031


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}

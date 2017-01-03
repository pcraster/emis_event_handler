import os


class Configuration:

    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")

    EMIS_SMTP_SERVER = os.environ.get("EMIS_SMTP_SERVER")
    EMIS_SMTP_PORT = os.environ.get("EMIS_SMTP_PORT")
    EMIS_SMTP_SENDER = os.environ.get("EMIS_SMTP_SENDER")


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    pass


class TestingConfiguration(Configuration):

    pass


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}

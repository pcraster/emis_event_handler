import os
from event_handler import create_app


app = create_app(os.getenv("EMIS_EVENT_HANDLER_CONFIGURATION"))

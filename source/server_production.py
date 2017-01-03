import os
os.environ["EMIS_EVENT_HANDLER_CONFIGURATION"] = "production"
from server import app


app.run(host="0.0.0.0")

import os

class Config:
    QUESTDB_CONF = os.getenv('QUESTDB_CONF', default="http::addr=localhost:9000;username=admin;password=quest;")

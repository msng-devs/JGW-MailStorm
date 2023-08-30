import os

from dotenv import load_dotenv
from src.helpers.path import get_absolute_path

load_dotenv(get_absolute_path([".env"]))


class Config:
    def __init__(self):
        self.collector_port = int(os.getenv("COLLECTOR_PORT"))
        self.worker_port = int(os.getenv("WORKER_PORT"))
        self.worker_pool_size = int(os.getenv("WORKER_POOL_SIZE"))
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_from = os.getenv("SMTP_FROM")


config = Config()


def validate_env():
    pass

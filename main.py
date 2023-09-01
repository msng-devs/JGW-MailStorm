import logging
import os
import shutil
from multiprocessing import Process

from src.core.worker import run_workers
from src.core.collector import run_collector
from src.helpers.config import config
from src.helpers.log import setup_logging
from src.model.model import init_db
from src.model.template import refresh_template_list, get
from src.helpers.path import get_absolute_path

setup_logging()


def init_data():
    data_path = get_absolute_path(['data', 'template'])
    bootstrap_path = get_absolute_path(['bootstrap', 'plain_text.html'])

    if not os.path.exists(data_path):
        logging.info("Initialize data directory")
        os.makedirs(data_path)
        shutil.copy(bootstrap_path, data_path)


if __name__ == '__main__':

    init_db()
    init_data()
    result = refresh_template_list()
    if not result:
        exit(1)

    Process(target=run_collector, args=(config.collector_port,)).start()
    run_workers(config.worker_pool_size, config.worker_port, config.collector_port)

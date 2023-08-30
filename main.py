import logging
from multiprocessing import Process

from src.core.worker import run_workers
from src.core.collector import run_collector
from src.helpers.config import config
from src.helpers.log import setup_logging
from src.model.model import init_db
from src.model.template import refresh_template_list, get
setup_logging()
if __name__ == '__main__':

    init_db()
    result = refresh_template_list()
    if not result:
        exit(1)

    Process(target=run_collector, args=(config.collector_port,)).start()
    run_workers(config.worker_pool_size, config.worker_port, config.collector_port)

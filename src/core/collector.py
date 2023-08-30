import zmq
import logging

from src.helpers.json_convert import convert_result_res
import src.model.history as history


def run_collector(port: int):
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind(f"tcp://127.0.0.1:{port}")

    logging.info(f"[Collector] collector started in port {port}")
    while True:
        result = results_receiver.recv_json()
        try:
            process_create_history(str(result))
        except Exception as e:
            logging.error(f"[Collector] collector error: {str(e)}")


def process_create_history(message: str):
    result = convert_result_res(message)
    logging.info(f"[Collector] result worker {result.worker_id} : template {result.template} / status {result.status} / message {result.message}")
    history.create(result)

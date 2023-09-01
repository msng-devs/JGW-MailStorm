import logging

import zmq


def run_streamer(port: int, worker_port):
    context = zmq.Context()

    # 받는 포트
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind(f"tcp://*:{port}")

    # Worker로 보내는 포트
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{worker_port}")

    logging.info(f"[Streamer] streamer started in port {port}")

    zmq.device(zmq.STREAMER, pull_socket, push_socket)

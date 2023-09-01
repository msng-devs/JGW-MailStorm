import json
import logging
from multiprocessing import Process

import zmq
import src.model.template as template
from src.core.mail import send_mail
from src.core.template import render
from src.helpers.exception import JsonValidationException, TemplateFormatException
from src.helpers.json_convert import convert_mail_req, MailReq, Result
from src.helpers.path import get_absolute_path


class ProcessResult:
    def __init__(self, status: bool, message: str, req: MailReq = None):
        self.status = status
        self.message = message
        self.req = req


def run_worker(worker_id: str, port: int, collector_port: int):
    context = zmq.Context()

    work_receiver = context.socket(zmq.PULL)
    work_receiver.connect(f"tcp://0.0.0.0:{port}")

    collector_sender = context.socket(zmq.PUSH)
    collector_sender.connect(f"tcp://127.0.0.1:{collector_port}")

    poller = zmq.Poller()
    poller.register(work_receiver, zmq.POLLIN)

    logging.info(f"[Worker] worker {worker_id} started")
    while True:
        sockets = dict(poller.poll())
        if sockets.get(work_receiver) == zmq.POLLIN:
            message = work_receiver.recv_json()
            try:
                process_request(message, collector_sender, worker_id)
            except Exception as e:
                logging.error(f"[Worker] worker {worker_id} error: {str(e)}")


def run_workers(pool_size: int, port: int, collector_port: int):
    for i in range(pool_size):
        Process(target=run_worker, args=(i, port, collector_port)).start()


def process_request(message, collector_sender, worker_id):
    logging.debug(f"[Worker] worker {worker_id} received request : {message}")
    result = run_mail_send(str(message))
    send_history(result, collector_sender, worker_id)


def send_history(message: ProcessResult, collector_sender, worker_id):
    history_message = None
    if message.req is not None:
        history_message = Result(message.status, message.message, message.req, worker_id)
    else:
        history_message = Result(message.status, message.message, None, worker_id)
    collector_sender.send_json(history_message.to_json())


def run_mail_send(request: str) -> ProcessResult:
    req = None

    # 받은 request 변환하기
    try:
        req = convert_mail_req(request.replace("'", "\""))
    except JsonValidationException as e:
        return ProcessResult(False, str(e), None)
    except Exception as e:
        return ProcessResult(False, str(e), None)

    # 템플릿 정보 조회
    template_arg = None
    try:
        target_template = template.get(req.template)
        assert target_template is not None
        template_arg = target_template[-1]

    except AssertionError:
        return ProcessResult(False, f"Template {req.template} is not found", req)

    except Exception as e:
        return ProcessResult(False, str(e), req)

    # 메일 본문 렌더링
    render_content = None
    try:
        path = get_absolute_path(["data", "template", req.template + ".html"])
        rendered_content = render(path, template_arg.split(";"), req.arg)

    except TemplateFormatException as e:
        return ProcessResult(False, str(e), req)

    except Exception as e:
        return ProcessResult(False, str(e), req)

    # 메일 실제 발송
    try:
        send_mail(req.to, req.subject, rendered_content)
    except Exception as e:
        return ProcessResult(False, str(e), req)

    return ProcessResult(True, "Success", req)

import json
import logging
import re
from src.helpers.exception import JsonValidationException


class MailReq:
    def __init__(self):
        self.to = ""
        self.subject = ""
        self.template = ""
        self.arg = ""
        self.who = ""

    def validate(self):
        if not self.who:
            raise JsonValidationException("'who' field is required")

        if not self.to:
            raise JsonValidationException("'to' field is required")

        if not self.subject:
            raise JsonValidationException("'subject' field is required")

        if not self.arg:
            raise JsonValidationException("'arg' field is required")

        if not self.template:
            raise JsonValidationException("'template' field is required")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.to):
            raise JsonValidationException("Invalid 'to' email format")

        if not isinstance(self.arg, dict):
            raise JsonValidationException("'arg' must be a dictionary")

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def __str__(self):
        return self.to_json()


class Result:
    def __init__(self, status: bool = False, message: str = "", req: MailReq = None, worker_id: str = ""):

        if req is not None:
            self.recipient = req.to
            self.subject = req.subject
            self.template = req.template
            self.arg = req.arg
            self.service = req.who
        else:
            self.recipient = "unknown"
            self.subject = "unknown"
            self.template = "unknown"
            self.arg = {}
            self.service = "unknown"

        self.status = status
        self.message = message
        self.worker_id = worker_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def to_arg_json(self):
        return json.dumps(self.arg, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def __str__(self):
        return self.to_json()


def convert_mail_req(json_str: str) -> MailReq:
    try:
        json_dict = json.loads(json_str)
    except ValueError as e:
        logging.error(e)
        raise JsonValidationException("Invalid json format")

    mail_req = MailReq()

    if "who" in json_dict:
        mail_req.who = json_dict["who"]

    if "to" in json_dict:
        mail_req.to = json_dict["to"]

    if "subject" in json_dict:
        mail_req.subject = json_dict["subject"]

    if "arg" in json_dict:
        mail_req.arg = json_dict["arg"]

    if "template" in json_dict:
        mail_req.template = json_dict["template"]

    mail_req.validate()

    return mail_req


def convert_result_res(json_str: str) -> Result:
    json_dict = None
    try:
        json_dict = json.loads(json_str)
    except ValueError as e:
        raise JsonValidationException("Invalid json format")

    result = Result()

    result.recipient = json_dict["recipient"]
    result.subject = json_dict["subject"]
    result.template = json_dict["template"]
    result.arg = json_dict["arg"]
    result.service = json_dict["service"]
    result.status = json_dict["status"]
    result.message = json_dict["message"]
    result.worker_id = json_dict["worker_id"]
    result.template = json_dict["template"]

    return result

from jinja2 import Environment, FileSystemLoader, Template

from src.helpers.exception import TemplateFormatException

env = Environment(loader=FileSystemLoader("."))


def render(path: str, template_arg: list, arg: dict) -> str:
    validate(template_arg, arg)
    with open(path, "r") as template_file:
        template_content = template_file.read()
        template = Template(template_content)

    return template.render(arg)


def validate(template_arg: list, arg: dict):
    for key in template_arg:
        if key not in arg.keys():
            raise TemplateFormatException(f"The template requires the {key} argument")


def parse(path: str) -> str:
    with open(path, "r") as template_file:
        args_line = template_file.readline().strip()
        if args_line.startswith("<!--") and args_line.endswith("-->"):
            data = args_line[4:-3]
        else:
            raise TemplateFormatException("템플릿 형식이 잘못되었습니다.")
    return data

from jinja2 import Environment
from jinja2 import FileSystemLoader


class AtomRenderer(object):
    def __init__(self, template_path):
        self.environment = Environment(
            loader=FileSystemLoader(template_path)
        )

    def render(self, data, template):
        t = self.environment.get_template(template)
        return t.render(data.to_dict())

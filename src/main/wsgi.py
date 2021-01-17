import sentry_sdk

from framework.dirs import DIR_SRC
from framework.util.settings import get_setting

sentry_sdk.init(get_setting("SENTRY_DSN"), traces_sample_rate=1.0)


def application(environ, start_response):
    if environ["PATH_INFO"] == "/e/":
        division = 1 / 0
    elif environ["PATH_INFO"] == "/about/":
        template = read_template("about.html")
    else:
        template = read_template("index.html")

    status = "200 OK"

    headers = {
        "Content-type": "text/html",
    }

    environ2 = ""

    for key in environ:
        value = environ[key]
        text = f"<p><b>{key}</b> : {value}</p>"
        environ2 += text

    payload = template.format(
        environ=environ2,
    )

    start_response(status, list(headers.items()))

    yield payload.encode()


def read_template(template_name):
    dir_templates = DIR_SRC / "main" / "templates"
    template = dir_templates / template_name

    assert template.exists() and template.is_file()

    with template.open("r") as fd:
        content = fd.read()

    return content

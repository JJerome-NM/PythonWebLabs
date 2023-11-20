import platform

from flask import render_template, request


def enumerate_filter(iterable):
    return enumerate(iterable)

def base_render(template: str, **context):
    return render_template(template, about_os=platform.platform(), user_agent_info=request.user_agent.string, **context)

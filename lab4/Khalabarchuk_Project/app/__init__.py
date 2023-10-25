from flask import Flask


def enumerate_filter(iterable):
    return enumerate(iterable)


app = Flask(__name__)
app.secret_key = b"secret"

app.jinja_env.filters['enumerate'] = enumerate_filter


from app import views

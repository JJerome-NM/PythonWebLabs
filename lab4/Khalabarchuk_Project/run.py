from os import environ

from app import app


if __name__ == '__main__':
    app.run(port=environ.get("PORT") or "5000", host=environ.get("HOST") or "localhost")

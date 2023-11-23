from flask import current_app as app, redirect, url_for


@app.route("/")
def main():
    return redirect(url_for("common.portfolio_main"))


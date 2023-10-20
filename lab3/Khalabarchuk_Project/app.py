from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/portfolio')
def portfolio_main():
    return render_template("portfolio-main.html")


@app.route('/projects')
def portfolio_projects():
    return render_template("portfolio-projects.html")


@app.route('/contacts')
def portfolio_contacts():
    return render_template("portfolio-contacts.html")


if __name__ == '__main__':
    app.run(debug=True)

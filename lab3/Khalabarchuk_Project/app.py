from flask import Flask, render_template, request, url_for

PROJECTS_LIST = list([
    {"photo_url": "projectNMWS.png",
     "name": "NM-WebSockets",
     "project_url": "https://github.com/JJerome-NM/NM-WebSockets"
     },
    {"photo_url": "projectCodenames.png",
     "name": "CodeNames",
     "project_url": "https://github.com/JJerome-NM/CodeNames"
     },
    {"photo_url": "projectWSHelper.png",
     "name": "WebSocketHelper",
     "project_url": "https://github.com/JJerome-NM/WebSocketHelper"
     }]
)

CONTACTS = [{
        "type": "EMAIL",
        "contact_name": "Gmail",
        "name": "Mykhailo Khalabarchuk",
        "link": "mykhailo.khalabarchuk.21@pnu.edu.ua",
        "title": "JJerome-NM"
    }, {
        "type": "DEFAULT",
        "contact_name": "Linkedin",
        "name": "Mykhailo Khalabarchuk",
        "link": "https://www.linkedin.com/in/mykhailo-khalabarchuk-26376528b/",
        "title": "Mykhailo Khalabarchuk"
    }, {
        "type": "DEFAULT",
        "contact_name": "Github",
        "name": "Михайло Халабарчук",
        "link": "https://github.com/JJerome-NM",
        "title": "Михайло Халабарчук"
    }]

app = Flask(__name__)


@app.route('/')
@app.route('/portfolio')
def portfolio_main():
    return render_template("portfolio-main.html")


@app.route('/projects')
def portfolio_projects():
    return render_template("portfolio-projects.html", projects_list=PROJECTS_LIST)


@app.route('/contacts')
def portfolio_contacts():
    return render_template("portfolio-contacts.html", contacts=CONTACTS)


if __name__ == '__main__':
    app.run(debug=True)

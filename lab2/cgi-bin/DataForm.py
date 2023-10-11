import os
from http.cookies import SimpleCookie


class Labels:
    NAME = "name"
    LASTNAME = "lastname"
    GENDER = "gender"
    CAR = "car"


cookie = SimpleCookie(os.environ.get("HTTP_COOKIE"))


def get_cookie_or_else_default(label: str, default):
    val = cookie.get(label)
    return val.value if val and val.value is not None else default


name_cookie = get_cookie_or_else_default("name", "")
lastname_cookie = get_cookie_or_else_default("lastname", "")
gender_cookie = get_cookie_or_else_default("gender", "")

print("""
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Input form</title>
</head>

<style>

    .main-form {
        display: flex;

        flex-direction: column;
        flex-wrap: wrap;

        width: min-content;
    }

    .fieldset-block {
        margin: 10px;

        width: max-content;
    }

</style>
""" + f"""
<body>
    <form action="DataFormHandler.py" type="POST" class="main-form">
        <label>
            <span>Name:</span>
            <input name="{Labels.NAME}" value="{name_cookie}" placeholder="Prepparato">
        </label>
        <label>
            <span>Lastname:</span>
            <input name="{Labels.LASTNAME}" value="{lastname_cookie}" placeholder="Secondnissimo">
        </label>
    
        <fieldset class="fieldset-block">
            <legend>Choose your gender</legend>
    
            <div>
                <input type="radio" id="gender-male" name="{Labels.GENDER}" value="Male" {"checked" if gender_cookie == "Male" else ""}/>
                <label for="gender-male">Male</label>
            </div>
            <div>
                <input type="radio" id="gender-female" name="{Labels.GENDER}" value="Female" {"checked" if gender_cookie == "Female" else ""}/>
                <label for="gender-female">Female</label>
            </div>
            <div>
                <input type="radio" id="gender-croissant" name="{Labels.GENDER}" value="Croissant" {"checked" if gender_cookie == "Croissant" else ""}/>
                <label for="gender-croissant">Croissant</label>
            </div>
        </fieldset>
    
        <fieldset class="fieldset-block">
            <legend>Choose your best cars</legend>
            <div>
                <input type="checkbox" id="car-porsche" name="{Labels.CAR}" value="Porsche"/>
                <label for="car-porsche">Porsche</label>
            </div>
            <div>
                <input type="checkbox" id="car-bmw" name="{Labels.CAR}" value="BMW"/>
                <label for="car-bmw">BMW</label>
            </div>
            <div>
                <input type="checkbox" id="car-audi" name="{Labels.CAR}" value="Audi"/>
                <label for="car-audi">Audi</label>
            </div>
            <div>
                <input type="checkbox" id="car-something-else" name="{Labels.CAR}" value="Something else"/>
                <label for="car-something-else">Something else</label>
            </div>
        </fieldset>
    
        <button type="submit">Submit</button>
    </form>
</body>
</html>
""")

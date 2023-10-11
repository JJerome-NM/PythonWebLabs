from cgi import FieldStorage
from http.cookies import SimpleCookie


class Labels:
    NAME = "name"
    LASTNAME = "lastname"
    GENDER = "gender"
    CAR = "car"
    CLEAR_COOKIES = "clear_cookies"


fields = FieldStorage()

name: str = fields.getfirst(Labels.NAME)
lastname: str = fields.getfirst(Labels.LASTNAME)
gender: str = fields.getfirst(Labels.GENDER)
cars: list[str] = fields.getvalue(Labels.CAR)

if name is not None:
    print(f"Set-cookie: name={name};")
if lastname is not None:
    print(f"Set-cookie: lastname={lastname};")
if gender is not None:
    print(f"Set-cookie: gender={gender};")

should_clear_cookie: bool = bool(fields.getvalue(Labels.CLEAR_COOKIES))


if should_clear_cookie:
    cookie = SimpleCookie()

    cookie["name"] = ""
    cookie["name"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["lastname"] = ""
    cookie["lastname"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["gender"] = ""
    cookie["gender"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"

    print(cookie.output())

print(f"""

<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>DataFormHandler</title>
</head>
<body>
    <h2>Hello {name if name else "User"} thank you for filling out the form, here are your details:</h2>
    <h3>Name - {name if name else "I dont now"}</h3>
    <h3>Lastname - {lastname if lastname else "I dont now"}</h3>
    <h3>Gender - {gender if gender else "I dont now"}</h3>
    <h3>Cars:</h3>
    {f'<ul><li>{"</li><li>".join(cars)}</li></ul>' if cars else "You have not chosen anyone"}

    <form>
        <input type="hidden" name="name" value="{name if gender else ""}">
        <input type="hidden" name="lastname" value="{lastname if gender else ""}">
        <input type="hidden" name="gender" value="{gender if gender else ""}">
        {"".join([f" <input type='hidden' name='car' value='{car}'>" for car in cars]) if cars else ""}
        <input type="hidden" name="clear_cookies" value="{'false' if should_clear_cookie else 'true'}">
        
        <button type="submit">Clear cookies</button>
    </form>
</body>
</html>

""")

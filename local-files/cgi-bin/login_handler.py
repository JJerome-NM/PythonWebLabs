import cgi

form = cgi.FieldStorage()

username = form['username'].value
password = form['password'].value

if username == "admin" and password == "admin":
    message = "Login successful"
else:
    message = "Нєєє то все фігня"

print(f"""
Content-type:text/html


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{message}
</body>
</html>
""")

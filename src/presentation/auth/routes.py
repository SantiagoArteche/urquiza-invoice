from flask import Blueprint, render_template, request

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get("username")
        password = request.form.get("password")
        if user == "admin" and password == "1234":
            message = "Login exitoso!"
        else:
            message = "Usuario o contraseña incorrectos"
        return render_template('login.html', message=message)
    
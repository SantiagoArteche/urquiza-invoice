from flask import Blueprint, render_template, request
from data.models.user import User

auth_bp = Blueprint("auth", __name__, template_folder='../templates')

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get("name")
        password = request.form.get("password")

        found_user = User.query.filter_by(name=name).first()

        error = False
        if not found_user or found_user is None:
            error = True
            message = 'Credenciales incorrectas'
       
        if not error and not found_user.check_password(password):
            error = True
            message = 'Credenciales incorrectas'
        
        if not error:
            return render_template('home.html')
        
        return render_template('login.html', message=message)
    
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        rol = request.form.get("rol")
        User.create(name, password, email, rol)

        return render_template('login.html', message='Usuario registrado exitosamente')

@auth_bp.route("/home", methods=['GET'])
def dashboard():
    return render_template('home.html')

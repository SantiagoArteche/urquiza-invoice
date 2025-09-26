from flask import Blueprint, render_template, request
from data.models.user import User
from data.models.client import Client
from data.models.product import Product
from data.models.invoice import Invoice
from datetime import datetime
from sqlalchemy import extract
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
current_date = datetime.now().strftime("%d de %B de %Y") 

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

@auth_bp.route("/home", methods=['GET', 'POST'])
def dashboard():
    clients = Client.query.all()
    products = Product.query.all()
    invoices = Invoice.query.all()
    today = datetime.today()
    this_month_invoices = (
        Invoice.query
        .filter(extract('year', Invoice.date) == today.year)
        .filter(extract('month', Invoice.date) == today.month)
        .all()
    )
    invoices_total = sum(invoice.total for invoice in invoices)
    return render_template('home.html', current_date=current_date, clients_length=len(clients), products_length=len(products), invoices_length=len(this_month_invoices), invoices_total=invoices_total)

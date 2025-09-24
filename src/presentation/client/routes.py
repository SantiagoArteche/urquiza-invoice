from flask import Blueprint, render_template, request, redirect, url_for
from data.models.client import Client
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
current_date = datetime.now().strftime("%d de %B de %Y") 

client_bp = Blueprint("client", __name__, template_folder='../templates')

@client_bp.route("/client", methods=['GET'])
def list():
    clients = Client.query.all()
    return render_template('client-list.html', clients=clients, current_date=current_date)

@client_bp.route("/client/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create-client.html')
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        
        error = False
        message = ""
        
        if not name or not email:
            error = True
            message = 'Nombre y email son campos obligatorios'
        
        if not error:
            client_exists = Client.query.filter_by(email=email).first()
            if client_exists:
                error = True
                message = 'Ya existe un cliente con ese email'
        
        if not error:
            try:
                Client.create(name, email, phone, address)
                return render_template('create-client.html', success_message='Cliente creado exitosamente')
            except Exception as e:
                error = True
                message = 'Error al crear el cliente'
        
        return render_template('create-client.html', message=message)

@client_bp.route("/client/edit/<int:client_id>", methods=['GET', 'POST'])
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'GET':
        return render_template('edit-client.html', client=client)
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        
        error = False
        message = ""
        print(client_id)
        if not name or not email:
            error = True
            message = 'Nombre y email son campos obligatorios'
        
        if not error:
            found_client = Client.query.filter_by(id=client_id).first()

            if found_client and found_client.id != client_id:
                error = True
        
        if not error:
            try:
                Client.update(found_client.id, {"name": name, "address": address, "phone": phone, "email": email})
                return redirect(url_for('client.list'))
            except Exception as e:
                error = True
        
        return redirect(url_for('client.list'))

@client_bp.route("/client/delete/<int:client_id>", methods=['POST'])
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    
    try:
        Client.delete(client=client)
        return redirect(url_for('client.list'))
    except Exception as e:
        return redirect(url_for('client.list'))

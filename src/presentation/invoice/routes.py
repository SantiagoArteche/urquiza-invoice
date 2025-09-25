from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from data.models.invoice import Invoice, InvoiceDetail
from data.models.client import Client
from data.models.product import Product
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
current_date = datetime.now().strftime("%d de %B de %Y") 

invoice_bp = Blueprint("invoice", __name__, template_folder='../templates')

@invoice_bp.route("/invoice", methods=['GET'])
def list():
    invoices = Invoice.query.all()
    return render_template('invoice-list.html', invoices=invoices, current_date=current_date)

@invoice_bp.route("/invoice/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        clients = Client.query.all()
        return render_template('create-invoice.html', clients=clients, datetime=datetime)
    else:
        client_id = request.form.get("client_id")
        date = request.form.get("date")
        
        error = False
        message = ""
        
        if not client_id:
            error = True
            message = 'Debe seleccionar un cliente'
        
        if not date:
            error = True
            message = 'La fecha es obligatoria'
        
        if not error:
            try:
                client_id = int(client_id)
                date = datetime.strptime(date, '%Y-%m-%d').date()
                
                client = Client.query.get(client_id)
                if not client:
                    error = True
                    message = 'Cliente no válido'
            except ValueError:
                error = True
                message = 'Datos no válidos'
        
        if not error:
            try:
                invoice = Invoice.create(client_id, date, 0)
                return redirect(url_for('invoice.edit', invoice_id=invoice.id))
            except Exception as e:
                error = True
                message = 'Error al crear la factura'
        
        clients = Client.query.all()
        return render_template('create-invoice.html', clients=clients, message=message)

@invoice_bp.route("/invoice/edit/<int:invoice_id>", methods=['GET', 'POST'])
def edit(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if request.method == 'GET':
        clients = Client.query.all()
        products = Product.query.all()
        details = InvoiceDetail.query.filter_by(invoice_id=invoice_id).all()
        return render_template('edit-invoice.html', invoice=invoice, clients=clients, products=products, details=details)
    else:
        client_id = request.form.get("client_id")
        date = request.form.get("date")
        
        error = False
        message = ""
        
        if not client_id or not date:
            error = True
            message = 'Cliente y fecha son campos obligatorios'
        
        if not error:
            try:
                client_id = int(client_id)
                date = datetime.strptime(date, '%Y-%m-%d').date()
                
                client = Client.query.get(client_id)
                if not client:
                    error = True
                    message = 'Cliente no válido'
            except ValueError:
                error = True
                message = 'Datos no válidos'
        
        if not error:
            try:
                Invoice.update(invoice.id, {"client_id": client_id, "date": date})
                invoice.calculate_total()
                return redirect(url_for('invoice.list'))
            except Exception as e:
                error = True
                message = 'Error al actualizar la factura'
        
        clients = Client.query.all()
        products = Product.query.all()
        details = InvoiceDetail.query.filter_by(invoice_id=invoice_id).all()
        return render_template('edit-invoice.html', invoice=invoice, clients=clients, products=products, details=details, message=message)

@invoice_bp.route("/invoice/delete/<int:invoice_id>", methods=['POST'])
def delete(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    try:
        Invoice.delete(invoice=invoice)
        return redirect(url_for('invoice.list'))
    except Exception as e:
        return redirect(url_for('invoice.list'))

@invoice_bp.route("/invoice/<int:invoice_id>/add-product", methods=['POST'])
def add_product(invoice_id):
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        unit_price = int(request.form.get('unit_price'))
        
        detail = InvoiceDetail.create(invoice_id, product_id, quantity, unit_price)
        
        invoice = Invoice.query.get(invoice_id)
        invoice.calculate_total()
        
        return redirect(url_for('invoice.edit', invoice_id=invoice_id))
    except Exception as e:
        return redirect(url_for('invoice.edit', invoice_id=invoice_id))

@invoice_bp.route("/invoice/detail/<int:detail_id>/remove", methods=['POST'])
def remove_product(detail_id):
    try:
        detail = InvoiceDetail.query.get_or_404(detail_id)
        invoice_id = detail.invoice_id
        
        InvoiceDetail.delete(detail)
        
        invoice = Invoice.query.get(invoice_id)
        invoice.calculate_total()
        
        return redirect(url_for('invoice.edit', invoice_id=invoice_id))
    except Exception as e:
        return redirect(url_for('invoice.edit', invoice_id=invoice_id))

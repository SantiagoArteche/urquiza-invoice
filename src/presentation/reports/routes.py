from flask import Blueprint, render_template, request, flash
from data.models.client import Client
from data.models.invoice_detail import InvoiceDetail
from data.models.invoice import Invoice
from data.models.client import Client
from data.mysql_db.init import database 
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
current_date = datetime.now().strftime("%d de %B de %Y") 

reports_bp = Blueprint("reports", __name__, template_folder='../templates')

@reports_bp.route("/reports", methods=['GET'])
def reports():
    clients = Client.query.all()
    return render_template('reports.html', clients=clients)


@reports_bp.route('/reports/client', methods=['POST'])
def client_report():
    try:
        client_id = request.form.get('client_id')
        
        if not client_id:
            flash('Debe seleccionar un cliente', 'error')
            clients = Client.query.all()
            return render_template('reports.html', clients=clients, message='Debe seleccionar un cliente')
        
        client_invoices = database.session.query(
            Invoice.id,
            Invoice.date,
            Client.name.label('client_name'),
            database.func.coalesce(database.func.sum(InvoiceDetail.quantity * InvoiceDetail.unit_price), 0).label('total')
        ).join(Client).outerjoin(InvoiceDetail).filter(
            Invoice.client_id == client_id
        ).group_by(Invoice.id, Invoice.date, Client.name).all()
        
        client_total = sum(invoice.total for invoice in client_invoices)
        
        clients = Client.query.all()
        
        return render_template('reports.html', clients=clients, client_invoices=client_invoices, client_total=client_total, selected_client_id=int(client_id))

    except Exception as e:
        flash(f'Error al generar el reporte: {str(e)}', 'error')
        clients = Client.query.all()
        return render_template('reports.html', clients=clients, message=f'Error al generar el reporte: {str(e)}')

@reports_bp.route('/reports/period', methods=['POST'])
def period_report():
    try:
        year = request.form.get('year')
        quarter = request.form.get('quarter')
        
        if not year or not quarter:
            flash('Debe seleccionar año y trimestre', 'error')
            clients = Client.query.all()
            return render_template('reports.html', clients=clients, message='Debe seleccionar año y trimestre')
        
        year = int(year)
        quarter = int(quarter)
        
        quarter_months = {
            1: [1, 2, 3],   
            2: [4, 5, 6],    
            3: [7, 8, 9],    
            4: [10, 11, 12]  
        }
        
        months = quarter_months[quarter]
        
        period_invoices = database.session.query(
            Invoice.id,
            Invoice.date,
            Client.name.label('client_name'),
            database.func.coalesce(database.func.sum(InvoiceDetail.quantity * InvoiceDetail.unit_price), 0).label('total')
        ).join(Client).outerjoin(InvoiceDetail).filter(
            database.extract('year', Invoice.date) == year,
            database.extract('month', Invoice.date).in_(months)
        ).group_by(Invoice.id, Invoice.date, Client.name).all()
        
        period_total = sum(invoice.total for invoice in period_invoices)
        period_count = len(period_invoices)
        
        clients = Client.query.all()
        
        return render_template('reports.html', clients=clients, period_data=True, period_invoices=period_invoices, 
                period_total=period_total, period_count=period_count, selected_year=year, selected_quarter=quarter)

    except Exception as e:
        flash(f'Error al generar el reporte: {str(e)}', 'error')
        clients = Client.query.all()
        return render_template('reports.html', clients=clients, message=f'Error al generar el reporte: {str(e)}')


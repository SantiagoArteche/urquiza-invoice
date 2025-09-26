from data.mysql_db.init import database
from data.models.client import Client
from data.models.invoice_detail import InvoiceDetail
from data.models.product import Product
from datetime import datetime

class Invoice(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    client_id = database.Column(database.Integer, database.ForeignKey('client.id'), nullable=False)
    date = database.Column(database.Date, nullable=False)
    total = database.Column(database.Integer, nullable=True)
    client = database.relationship('Client', backref='invoices')
    details = database.relationship('InvoiceDetail', backref='invoice', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Invoice {self.id}>'
    
    @classmethod
    def create(cls, client_id, date=None, total=0):
        if date is None:
            date = datetime.now().date()
        
        invoice = cls(client_id=client_id, date=date, total=total)
        database.session.add(invoice)
        database.session.commit()
        return invoice
    
    @classmethod
    def update(cls, invoice_id, data):
        invoice = cls.query.get(invoice_id)
        if invoice:
            for key, value in data.items():
                setattr(invoice, key, value)
            database.session.commit()
        return invoice
    
    @classmethod
    def delete(cls, invoice):
        try:
            database.session.delete(invoice)
            database.session.commit()
        except Exception:
            database.session.rollback()
            return False
    
    def calculate_total(self):
        total = sum(detail.subtotal for detail in self.details)
        self.total = total
        database.session.commit()
        return total
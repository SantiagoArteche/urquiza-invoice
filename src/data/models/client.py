from data.mysql_db.init import database
from data.models.invoice_detail import InvoiceDetail


class Client(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True, nullable=False)
    address = database.Column(database.String(120), nullable=False)
    phone = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(50), nullable=False)


    @classmethod
    def create(cls, name, address, email, phone):
        new_client = cls(name=name, address=address, email=email, phone=phone)
        database.session.add(new_client)
        database.session.commit()
        return new_client
    
    @classmethod
    def delete(cls, client):
        from data.models.invoice import Invoice
        found_invoices = Invoice.query.filter(Invoice.client_id == client.id).all()

        try:
            if(len(found_invoices)):
                for invoice in found_invoices:
                    found_invoices_detail = Invoice.query.filter(InvoiceDetail.invoice_id == invoice.id).all()
                    for invoice_detail in found_invoices_detail:
                        database.session.delete(invoice_detail)
                    database.session.delete(invoice)
                    
            database.session.delete(client)
            database.session.commit()
            return True
        except Exception:
            database.session.rollback()
            return False

    @classmethod
    def update(cls, client_id, new_data: dict):
        try:
            updated = cls.query.filter_by(id=client_id).update(new_data)
            if not updated:
                return False 
            database.session.commit()
            return True
        except Exception:
            database.session.rollback()
            return False

    def __repr__(self):
        return f'<Client {self.name}>'
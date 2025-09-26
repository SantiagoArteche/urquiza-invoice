from data.mysql_db.init import database
from data.models.invoice_detail import InvoiceDetail

class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(80), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    stock = database.Column(database.Integer, nullable=False)

    @classmethod
    def create(cls, description, price, stock):
        new_product = cls(description=description, price=price, stock=stock)
        database.session.add(new_product)
        database.session.commit()
        return new_product
    
    @classmethod
    def delete(cls, product):
        found_invoices_detail = InvoiceDetail.query.filter(InvoiceDetail.product_id == product.id).all()
        
        try:
            if(len(found_invoices_detail)):
                for invoice_detail in found_invoices_detail:
                    database.session.delete(invoice_detail)

            database.session.delete(product)
            database.session.commit()
            return True
        except Exception:
            database.session.rollback()
            return False

    @classmethod
    def update(cls, product_id, new_data: dict):
        try:
            updated = cls.query.filter_by(id=product_id).update(new_data)
            if not updated:
                return False 
            database.session.commit()
            return True
        except Exception:
            database.session.rollback()
            return False

    def __repr__(self):
        return f'<Product {self.description}>'
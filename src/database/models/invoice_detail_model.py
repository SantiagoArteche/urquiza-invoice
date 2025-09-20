from database.mysql_database import database

class InvoiceDetail(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    invoice_id = database.Column(database.Integer, database.ForeignKey('invoice.id'),  nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    quantity =  database.Column(database.Integer, nullable=False)
    unit_price= database.Column(database.Integer, nullable=False)
    subtotal = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.description}>'  
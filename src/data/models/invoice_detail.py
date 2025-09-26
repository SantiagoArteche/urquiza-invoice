from data.mysql_db.init import database

class InvoiceDetail(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    invoice_id = database.Column(database.Integer, database.ForeignKey('invoice.id'), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    unit_price = database.Column(database.Integer, nullable=False)
    subtotal = database.Column(database.Integer, nullable=False)
    product = database.relationship('Product', backref='invoice_details')

    @classmethod
    def create(cls, invoice_id, product_id, quantity, unit_price):
        subtotal = quantity * unit_price
        detail = cls(
            invoice_id=invoice_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        database.session.add(detail)
        database.session.commit()
        return detail
    
    @classmethod
    def update(cls, detail_id, data):
        detail = cls.query.get(detail_id)
        if detail:
            for key, value in data.items():
                setattr(detail, key, value)
            if 'quantity' in data or 'unit_price' in data:
                detail.subtotal = detail.quantity * detail.unit_price
            database.session.commit()
        return detail
    
    @classmethod
    def delete(cls, detail):
        database.session.delete(detail)
        database.session.commit()


    def __repr__(self):
        return f'<InvoiceDetail {self.id}>'
from data.mysql_db.init import database

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
        try:
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
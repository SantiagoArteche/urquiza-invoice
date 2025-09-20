from database.mysql_database import database

class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(80), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    stock = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.description}>'
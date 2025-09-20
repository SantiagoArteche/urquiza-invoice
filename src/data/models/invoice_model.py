from data.mysql_db.init import database

class Invoice(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    client_id = database.Column(database.Integer, database.ForeignKey('client.id'), nullable=False)
    date = database.Column(database.Date, nullable=False)
    total = database.Column(database.Integer, nullable=True)

    def __repr__(self):
        return f'<Product {self.description}>'
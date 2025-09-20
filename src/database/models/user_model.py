from database.mysql_database import database

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(120), nullable=False)
    email = database.Column(database.String(80), nullable=False)
    rol = database.Column(database.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
from data.mysql_db.init import database
from werkzeug.security import generate_password_hash, check_password_hash

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(400), nullable=False)
    email = database.Column(database.String(80), nullable=False)
    rol = database.Column(database.String(50), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create(cls, name, password, email, rol):
        new_user = cls(name=name, email=email, rol=rol)
        new_user.set_password(password)
        database.session.add(new_user)
        database.session.commit()
        return new_user
    
    def __repr__(self):
        return f'<User {self.username}>'
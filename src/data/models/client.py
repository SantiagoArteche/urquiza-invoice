from data.mysql_db.init import database

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
        try:
            database.session.delete(client)
            database.session.commit()
            return True
        except Exception:
            database.session.rollback()   # revertimos si hay error
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
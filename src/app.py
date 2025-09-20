import os
from flask import Flask
from presentation.auth.routes import auth_bp
from data.mysql_db.init import database
from data.models.client_model import Client
from data.models.invoice_model import Invoice
from data.models.invoice_detail_model import InvoiceDetail
from data.models.product_model import Product
from data.models.user_model import User

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
database.init_app(app)

app.register_blueprint(auth_bp)

@app.route("/")
def running():
    return "<p>The server is running</p>"

if __name__ == "__main__":
    app.run(debug=True)


with app.app_context():
    database.create_all()
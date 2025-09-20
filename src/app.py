import os
from flask import Flask
from login.routes import login_bp
from database.mysql_database import database
from database.models.client_model import Client
from database.models.invoice_model import Invoice
from database.models.invoice_detail_model import InvoiceDetail
from database.models.product_model import Product
from database.models.user_model import User

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(login_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

@app.route("/")
def running():
    return "<p>The server is running</p>"

if __name__ == "__main__":
    app.run(debug=True)

database.init_app(app)

with app.app_context():
    database.create_all()
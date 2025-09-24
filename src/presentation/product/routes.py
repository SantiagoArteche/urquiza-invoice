from flask import Blueprint, render_template, request, redirect, url_for
from data.models.product import Product
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
current_date = datetime.now().strftime("%d de %B de %Y") 

product_bp = Blueprint("product", __name__, template_folder='../templates')

@product_bp.route("/product", methods=['GET'])
def list():
    products = Product.query.all()
    return render_template('product-list.html', products=products, current_date=current_date)

@product_bp.route("/product/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create-product.html')
    else:
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        
        error = False
        message = ""
        
        if not description or not price or not stock:
            error = True
            message = 'Descripción, precio y stock son campos obligatorios'
        
        if not error:
            try:
                price = int(price)
                stock = int(stock)
                if price < 0 or stock < 0:
                    error = True
                    message = 'El precio y stock deben ser números positivos'
            except ValueError:
                error = True
                message = 'El precio y stock deben ser números válidos'
        
        if not error:
            product_exists = Product.query.filter_by(description=description).first()
            if product_exists:
                error = True
                message = 'Ya existe un producto con esa descripción'
        
        if not error:
            try:
                Product.create(description, price, stock)
                return render_template('create-product.html', success_message='Producto creado exitosamente')
            except Exception as e:
                error = True
                message = 'Error al crear el producto'
        
        return render_template('create-product.html', message=message)

@product_bp.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'GET':
        return render_template('edit-product.html', product=product)
    else:
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        
        error = False
        message = ""
        
        if not description or not price or not stock:
            error = True
            message = 'Descripción, precio y stock son campos obligatorios'
        
        if not error:
            try:
                price = int(price)
                stock = int(stock)
                if price < 0 or stock < 0:
                    error = True
                    message = 'El precio y stock deben ser números positivos'
            except ValueError:
                error = True
                message = 'El precio y stock deben ser números válidos'
        
        if not error:
            found_product = Product.query.filter_by(id=product_id).first()

            if found_product and found_product.id != product_id:
                error = True
        
        if not error:
            try:
                Product.update(found_product.id, {"description": description, "price": price, "stock": stock})
                return redirect(url_for('product.list'))
            except Exception as e:
                error = True
        
        return redirect(url_for('product.list'))

@product_bp.route("/product/delete/<int:product_id>", methods=['POST'])
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        Product.delete(product=product)
        return redirect(url_for('product.list'))
    except Exception as e:
        return redirect(url_for('product.list'))

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from sqlalchemy_utils import database_exists, create_database

DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'TEST'
DB_ECHO = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(50))
    amount = db.Column(db.Integer)
    comment = db.Column(db.String(100))

    # выбираем объект из класса и выдается сам объект и id
    def __repr__(self):
        return '<Product %r>' % self.id


if not database_exists(db.engine.url):
    create_database(db.engine.url)

product1 = Product(id=1, name='milk', price=1.5, amount=10, comment='Belarus')
product2 = Product(id=2, name='banana', price=2.3, amount=20, comment='Africa')
product3 = Product(id=3, name='apple', price=2.0, amount=30, comment='Poland')

# db.session.add_all()
db.session.commit()
db.init_app(app)
db.create_all()


@app.route('/products')
def products():
    prod = Product.query.all()  # обращение к классу БД
    return render_template("task_17_1.html", prod=prod)


@app.route('/products/<int:id>')
def product_detail(id):
    prod_n = Product.query.get(id)
    return render_template("task_17_1_product_detail.html", prod_n=prod_n)


@app.route('/create_product', methods=['POST', 'GET'])
def create_product():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        amount = request.form['amount']
        comment = request.form['comment']

        product = Product(id=id, name=name, price=price, amount=amount, comment=comment)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/products')
        except:
            return "При добавлении продукта произошла ошибка"
    else:
        return render_template("task_17_1_create_product.html")


@app.route('/products/<int:id>/del')
def product_del(id):
    prod = Product.query.get_or_404(id)
    try:
        db.session.delete(prod)
        db.session.commit()
        return redirect('/products')
    except:
        return "При удалении произошла ошибка"

@app.route('/products/<int:id>/update', methods=['POST', 'GET'])
def create_update(id):
    prod = Product.query.get(id)
    if request.method == "POST":
        prod.id = request.form['id']
        prod.name = request.form['name']
        prod.price = request.form['price']
        prod.amount = request.form['amount']
        prod.comment = request.form['comment']

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "При обновлении продукта произошла ошибка"
    else:
        return render_template("task_17_1_update_product.html", prod=prod)


if __name__ == '__main__':
    app.run(debug=True)

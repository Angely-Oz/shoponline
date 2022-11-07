from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Text(50), nullable=False)
    amount = db.Column(db.Text(50), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


def __repr__(self):
    return self.title


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/price')
def price():
    products = Product.query.order_by(Product.price).all()
    return render_template('price.html', data = products)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        unit = request.form['unit']
        amount = request.form['amount']
        product = Product (title=title, description=description, price=price, unit=unit, amount=amount)
        try:
             db.session.add(product)
             db.session.commit()
             return redirect('/price')
        except:
            return "Произошла ошибка"
    else:
        return render_template('add_product.html')


@app.route('/buy/<int:id>')
def buy(id):
    product = Product.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(product.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
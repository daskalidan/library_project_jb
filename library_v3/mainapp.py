from flask import Flask, render_template

from books_manage import books
from customers_manage import customers
from loans_manage import loans
from DAL import *
app = Flask(__name__)

app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(loans)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('layout.html')





if __name__ == '__main__':
    app.run(debug=True)

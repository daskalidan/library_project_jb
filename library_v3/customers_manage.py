
from flask import Blueprint, render_template, request

from DAL import Customer


customers = Blueprint('customers',__name__,url_prefix='/customers')

@customers.route('/all')
def all_customers():
    customers_data = Customer.display_all_customers()
    return render_template('customers.html', data=customers_data)


@customers.route('/spesific', methods=['POST'])    
def looked_customer():
    look_name = request.form.get('look_name')
    print(look_name)
    looked_customer_data = Customer.display_customer(look_name)
    return render_template('customers.html', data=looked_customer_data)

@customers.route('/add', methods=['POST'])
def add_customer():
    id_number = request.form.get('id_number')
    name = request.form.get('name')
    city_address = request.form.get('city_address')
    age = request.form.get('age')
    Customer.add_customer(id_number, name, city_address, age)
    return all_customers()

@customers.route('/remove/<id_number>')
def remove_customer(id_number):
    Customer.remove_customer(id_number)
    return all_customers()
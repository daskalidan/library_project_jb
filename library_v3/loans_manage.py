
from flask import Blueprint, render_template, request

from DAL import Loan

loans = Blueprint('loans',__name__,url_prefix='/loans')


@loans.route('/all')
def all_loans():
    loans_data = Loan.display_all_loans()
    return render_template('loans.html', data=loans_data)

@loans.route('/late')
def late_loans():
    loans_data = Loan.display_all_late()
    return render_template('loans.html', data=loans_data)

@loans.route('/for_book', methods=['POST'])    
def loans_for_book():
    pass   

@loans.route('/for_customer', methods=['POST'])    
def loans_for_customer():
    pass   

@loans.route('/return/<cat_num>')
def return_loaned_book(cat_num):
    Loan.return_loaned(cat_num)
    return all_loans()
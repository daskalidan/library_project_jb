
from flask import Blueprint, render_template, request

from DAL import Book


books = Blueprint('books',__name__,url_prefix='/books')

@books.route('/all')
def all_books():
    books_data = Book.display_all_books()
    return render_template('books.html', data=books_data)

@books.route('/spesific', methods=['POST'])    
def looked_book():
    look_name = request.form.get('look_name')
    print(look_name)
    looked_books_data = Book.display_book(look_name)
    return render_template('books.html', data=looked_books_data)

@books.route('/add', methods=['POST'])
def add_book():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    book_type = request.form.get('book_type')
    Book.add_book(book_name, author, book_type)
    return all_books()

@books.route('/remove/<cat_num>')
def remove_book(cat_num):
    Book.remove_book(cat_num)
    return all_books()

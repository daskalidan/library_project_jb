from datetime import date, timedelta
from enum import Enum
import sqlite3


def database_query(sql_command, table):
    # access the database for a query and return list with the relevant data
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    cur.execute(f"SELECT name FROM pragma_table_info('{table}')")
    column_names = list(map(lambda name: name[0], cur.fetchall()))
    cur.execute(sql_command)
    details_list = [{column_names[index]:each[index] for index in range(len(column_names))} for each in cur.fetchall()]
    # print(details_list)
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    con.close()
    print(f'there are {count} {table}')
    return details_list


def database_update(sql_command, table):
    # access the database to update an existing table
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    try:
        cur.execute(sql_command)
        con.commit()
        con.close()
        return print(f"database table {table} has been changed")
    except:
        con.close()
        return print('database update failed')


class Book(Enum):

    # number of days to loan for each book type
    TYPE1 = 10
    TYPE2 = 5
    TYPE3 = 2
    BOOK_TYPES = {1: 10, 2: 5, 3: 2}

    def add_book(book_name, author, book_type, book_status='in library'):
        # add a new book to database table 'books'
        return database_update(f"INSERT INTO books (book_name, author, book_type, book_status) VALUES ('{book_name.lower()}', '{author.lower()}', '{book_type}', '{book_status}')", 'books')

    def loan_book(book_cat_num_to_loan):
        # change book status to 'loand' in database
        return database_update(f"UPDATE books SET book_status = 'loaned' WHERE cat_number = {book_cat_num_to_loan}", 'books')

    def return_book(book_to_return):
        # change book status to 'in library' in database
        return database_update(f"UPDATE books SET book_status = 'in library' WHERE cat_number = {book_to_return}", 'books')

    def display_all_books():
        # return a list with all books detailes
        return database_query(f'SELECT * FROM books', 'books')

    def display_book(look_name):
        # return a list with one book detailes
        return database_query(f"SELECT * FROM books WHERE book_name = '{look_name.lower()}'", 'books')

    def remove_book(book_to_remove):
        # change book status to removed only if book_status 'in library'
        # check if the chosen book to remove is in library
        chosen_book = database_query(f"SELECT * FROM books WHERE cat_number = '{book_to_remove}'", 'books')
        if chosen_book[0]['book_status'] != 'in library':
            return print(f'the chosen book {chosen_book[0]} is not in library and can not be removed')
        else:
            # if the chosen book to remove is in library chang the status to removed
            return database_update(f"UPDATE books SET book_status = 'removed' WHERE cat_number = '{book_to_remove}'", 'books')

class Customer():

    def add_customer(id_number, name, city_address, age, customer_status='active'):
        # try to add new customer to database
        return database_update(f"INSERT INTO customers (id_number, name, city_address, age, customer_status) VALUES ('{id_number}', '{name.lower()}', '{city_address.lower()}', '{age}', '{customer_status}')", 'customers')

    def display_all_customers():
        # return a list with all customers details
        return database_query(f'SELECT * FROM customers', 'customers')

    def display_customer(look_name):
        # return a list with one customer detailes
        return database_query(f"SELECT * FROM customers WHERE name = '{look_name.lower()}'", 'customers')

    def remove_customer(customer_to_remove):
        # chang customer status to 'inactive' only if all loans returned
        # check if customer has no open loanes
        status_list = []
        loans_for_customer = database_query(f"SELECT * FROM loans WHERE id_number = '{customer_to_remove}'", 'loans')
        for loan in loans_for_customer:
            status_list.append(loan['loan_status'])
        if 'open' in status_list or 'late' in status_list:
            return print(f'customer {customer_to_remove} has some open or late loans and can not be removed')
        else:
            database_update(f"UPDATE customers SET customer_status = 'inactive' WHERE id_number = '{customer_to_remove}'", 'customers')
            return print(f'customer {customer_to_remove} no longer active')


class Loan():
    

    def loan(loaner_id, book_cat_num_to_loan, loan_date=date.today()):
        # create a new loan only if customer allowed and book is in library
        #  check if customer is active
        con = sqlite3.connect('library_data.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM customers WHERE id_number = '{loaner_id}'")
        loaner = cur.fetchall()
        if loaner[0][4] != 'active':
            con.close()
            return print(f'customer {loaner_id} is not active/punished and can not loan a book')
        # check if book in library
        try:
            cur.execute(
                f"SELECT * FROM books WHERE cat_number = '{int(book_cat_num_to_loan)}'")
            book_to_loan = cur.fetchall()
            if book_to_loan[0][4] != 'in library':
                con.close()
                return print(f'book num {book_cat_num_to_loan} status is not "in library" and can not be loaned')
            else:
                book_type = book_to_loan[0][3]
                date_to_return = loan_date + timedelta(days=Book.BOOK_TYPES[book_type])
        except:
            con.close()
            return print('book number invalid')
        # creat a loan in database
        cur.execute(f"INSERT INTO loans(id_number, cat_number, loan_date, date_to_return, loan_status) \
                    VALUES('{loaner_id}', '{int(book_cat_num_to_loan)}', '{str(loan_date)}', '{str(date_to_return)}', 'open')")
        con.commit()
        con.close()
        # change book status to loand
        Book.loan_book(book_cat_num_to_loan)
        return print(f'customer id {loaner_id} loaned book number {book_cat_num_to_loan}.')

    def return_loaned(book_to_return):
        # chang loan loan status to 'returned'
        database_update(f"UPDATE loans SET loan_status = 'returned' WHERE cat_number = {book_to_return}", 'loans')
        # change book status back to 'in library'
        Book.return_book(book_to_return)
        return print(f'book number {book_to_return} has been returned')

    def display_all_loans():
        # return a list with all loans details
        return database_query(f'SELECT * FROM loans', 'loans')

    def display_all_late():
        # return a list with all loans details only for loans with loan_status late
        return database_query(f"SELECT * FROM loans WHERE loan_status = 'late'", 'loans')
        

    def display_loans_by_customer():
        pass

    def display_loans_by_book():
        pass

    def update_late():
        pass

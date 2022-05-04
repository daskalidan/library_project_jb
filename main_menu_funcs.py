import sqlite3
from datetime import *

BOOK_TYPES = {'1': 10, '2': 5, '3': 2}


def save_exit_0():
    """
    exit the program
    :return: None
    """
    print('byby. ')
    exit()


def add_new_customer_1():
    """
    get new customer info and add it to database
    :return: print of the relevant note
    """
    # get the info of the new customer
    id_number = input('Enter ID number: ')
    name = input('Enter customer name: ').lower()
    city_address = input("Enter customer's living city: ").lower()
    age = input("Enter customer's age: ")
    customer_status = 'active'
    # try to add new customer to database
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    try:
        cur.execute(
            f"INSERT INTO customers (id_number, name, city_address, age, customer_status) VALUES ('{id_number}', '{name}', '{city_address}', '{age}', '{customer_status}')")
        con.commit()
        con.close()
        return print('new customer added successfully')
    except:
        cur.execute(
            f"SELECT * FROM customers WHERE (id_number = '{id_number}')")
        print(cur.fetchall())
        con.close()
        return print(f'id number {id_number}, already exisst in library')


def add_new_book_2():
    """ get a new book info and add it to database"""
    # get the new book info
    book_name = input('Enter book name: ').lower()
    author = input("Enter author's name: ").lower()
    book_type = input("Enter book type (1/2/3): ")
    book_status = 'in library'
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    # try to add the new book to database
    try:
        cur.execute(
            f"INSERT INTO books (book_name, author, book_type, book_status) VALUES ('{book_name}', '{author}', '{book_type}', '{book_status}')")
        con.commit()
        con.close()
        return print('new book added successfully')
    except:
        return print('something happend, book not added')


def loan_book_3():
    """
    create a new loan only if customer allowed and book is in library
    :return:
    """
    loan_date = date.today()
    #  get customer's id number and check if customer is active
    loaner_id = input('Enter ID number: ')
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    cur.execute(f"SELECT * FROM customers WHERE id_number = '{loaner_id}'")
    loaner = cur.fetchall()
    if loaner[0][4] != 'active':
        con.close()
        return print(f'customer {loaner_id} is not active/punished and can not loan a book')
    # get book number and check if in library
    book_cat_num_to_loan = input('Enter catalog number: ')
    try:
        cur.execute(
            f"SELECT * FROM books WHERE cat_number = '{int(book_cat_num_to_loan)}'")
        book_to_loan = cur.fetchall()
        if book_to_loan[0][4] != 'in library':
            con.close()
            return print(f'book num {book_cat_num_to_loan} status is not "in library" and can not be loaned')
        else:
            book_type = book_to_loan[0][3]
            date_to_return = loan_date + timedelta(days=BOOK_TYPES[book_type])
    except:
        con.close()
        return print('book number invalid')
    # creat a loan in database
    cur.execute(f"INSERT INTO loans(id_number, cat_number, loan_date, date_to_return, loan_status) \
                VALUES('{loaner_id}', '{int(book_cat_num_to_loan)}', '{str(loan_date)}', '{str(date_to_return)}', 'open')")
    # change book status to loand
    cur.execute(f"UPDATE books SET book_status = 'loaned' WHERE cat_number = {int(book_cat_num_to_loan)}")
    con.commit()
    con.close()
    return print(f'customer id {loaner_id} loaned book number {book_cat_num_to_loan}.')


def return_book_4():
    # which book to return
    book_to_return = int(input('enter book catalog number to return: '))
    # change book status back to 'in library'
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    cur.execute(f"UPDATE books SET book_status = 'in library' WHERE cat_number = {book_to_return}")
    # chang loan loan status to 'returned'
    cur.execute(f"UPDATE loans SET loan_status = 'returned' WHERE cat_number = {book_to_return}")
    con.commit()
    con.close()
    return print(f'book number {book_to_return} has been returned')


def display_all_books_5():
    # print all books in database
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f'SELECT * FROM books'):
        print(row)
    cur.execute('SELECT COUNT(*) FROM books')
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} books')


def display_all_customers_6():
    # print all customers in database
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f'SELECT * FROM customers'):
        print(row)
    cur.execute('SELECT COUNT(*) FROM customers')
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} customers')


def display_all_loans_7():
    # print all loans in database
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f'SELECT * FROM loans'):
        print(row)
    cur.execute('SELECT COUNT(*) FROM loans')
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} loans')


def display_all_late_loans_8():
    # print all loans in database that have loan status 'late'
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f"SELECT * FROM loans WHERE loan_status = 'late'"):
        print(row)
    cur.execute("SELECT COUNT(*) FROM loans WHERE loan_status = 'late'")
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} late loans')


def display_loans_by_customer_9():
    """
    get a customer's id and display all the referred loans
    :return: a print of the relevant customer and all the relevant loans
    """
    look = input('enter customer id to display the relevant loans: ')
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f"SELECT * FROM loans WHERE id_number = '{look}'"):
        print(row)
    cur.execute(f"SELECT COUNT(*) FROM loans WHERE id_number = '{look}'")
    count = cur.fetchone()[0]
    con.close()
    return print(f'{look} has a total of {count} loans')


def display_loans_by_book_10():
    """
    gets book name and print all loans for this book 
    :return:
    """
    look = input("enter a book name to display all it's loans loans: ").lower()
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f"SELECT * FROM loans INNER JOIN books ON loans.cat_number = books.cat_number WHERE book_name = '{look}'"):
        print(row)
    cur.execute(
        f"SELECT COUNT(*) FROM loans INNER JOIN books ON loans.cat_number = books.cat_number WHERE book_name = '{look}'")
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} loans for the book named {look}')


def find_book_by_name_11():
    """
    print all books with the same name as the input given
    :return: None
    """
    look = input('which book are you looking?: ').lower()
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f"SELECT * FROM books WHERE book_name = '{look}'"):
        print(row)
    cur.execute(f"SELECT COUNT(*) FROM books WHERE book_name = '{look}'")
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} books by the name {look}')


def find_customer_by_name_12():
    """
    print all customers with the same name as the input given
    :return: None
    """
    look = input('which customer are you looking?: ').lower()
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    for row in cur.execute(f"SELECT * FROM customers WHERE name = '{look}'"):
        print(row)
    cur.execute(f"SELECT COUNT(*) FROM customers WHERE name = '{look}'")
    count = cur.fetchone()[0]
    con.close()
    return print(f'there are {count} customers by the name {look}')


def remove_book_13():
    """
    change book status to removed only if all copies status 'in library'
    :return: printed string with the relevant note
    """
    book_to_remove = input('which book you like to remove?: ').lower()
    # check if all copies of the chosen book to remove are in library
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    status_list = []
    for row in cur.execute(f"SELECT * FROM books WHERE book_name = '{book_to_remove}'"):
        print(row)
        status_list.append(row[4])
    print(status_list)
    if 'loaned' in status_list:
        con.close()
        return print(f'some copies of the book {book_to_remove} are loaned, the the book can not be removed')
    else:
        # if all copies are in library chang the status to removed
        cur.execute(f"UPDATE books SET book_status = 'removed' WHERE book_name = '{book_to_remove}'")
        con.commit()
        cur.execute(f"SELECT COUNT(*) FROM books WHERE book_name = '{book_to_remove}'")
        count = cur.fetchone()[0]
        con.close()
        return print(f'{count} copies of {book_to_remove} have been removed from library')


def remove_customer_14():
    """
    chang customer status to 'inactive' only if all loans returned
    :return:
    """
    to_remove = input('enter customer id to remove: ')
    # check if customer has no open loanes
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    status_list = []
    for row in cur.execute(f"SELECT * FROM loans WHERE id_number = '{to_remove}'"):
        print(row)
        status_list.append(row[4])
    if 'open' in status_list or 'late' in status_list:
        con.close()
        return print(f'customer {to_remove} has some open or late loans and can not be removed')
    else:
        cur.execute(f"UPDATE customers SET customer_status = 'inactive' WHERE id_number = '{to_remove}'")
        con.commit()
        con.close()
        return print(f'customer {to_remove} no longer active')


def choose_program(number):
    try:
        number = int(number)
        func_dict = {0: save_exit_0, 1: add_new_customer_1, 2: add_new_book_2, 3: loan_book_3, 4: return_book_4,
                     5: display_all_books_5, 6: display_all_customers_6, 7: display_all_loans_7,
                     8: display_all_late_loans_8, 9: display_loans_by_customer_9,
                     10: display_loans_by_book_10, 11: find_book_by_name_11, 12: find_customer_by_name_12,
                     13: remove_book_13, 14: remove_customer_14}
        return func_dict[number]()
    except ValueError:
        print('you did not enter a valid number')
    except KeyError:
        print('the number you entered does not exist in menu')

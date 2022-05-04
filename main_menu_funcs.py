from customers import *
from book import *
from loans import *
from main import customers_dict, books_dict, save_data, loans_list


def save_exit_0():
    """
    save the books, customers, loans data to pickle files and exit the program
    :return: None
    """
    save_data('customers_dump.pkl', customers_dict)
    save_data('books_dump.pkl', books_dict)
    save_data('loans_dump.pkl', loans_list)
    print('all your data is saved, byby. ')
    exit()


def add_new_customer_1():
    """
    create a new customer instance and add it to customers dict
    :return: print of the relevant note
    """
    # get the info of the new customer
    id_number = input('Enter ID number: ')
    name = input('Enter customer name: ')
    city_address = input("Enter customer's living city: ")
    age = input("Enter customer's age: ")

    # check if id already exists
    if id_number in customers_dict.keys():
        return print(f'id number: {id_number} already exists, customer not added.')
    else:  # add new customer
        temp = Customer(id_number, name, city_address, age)
        customers_dict[temp.get_id_number()] = temp
    save_data('customers_dump.pkl', customers_dict)
    return print('new customer added successfully')


def add_new_book_2():
    """ create a new book instance and add it to books dict"""
    # get the new book info
    book_name = input('Enter book name: ')
    author = input("Enter author's name: ")
    book_type = input("Enter book type (1/2/3): ")
    try:
        temp_type = {1: '', 2: '', 3: ''}
        a = temp_type[int(book_type)]
    except ValueError:
        return print('you did not enter a valid number, book not added')
    except KeyError:
        return print('the number you entered is not a valid book type, book not added')
    # add the new book
    temp = Book(book_name, author, book_type)
    books_dict[temp.get_cat_number()] = temp
    save_data('books_dump.pkl', books_dict)
    return print('new book added successfully')


def loan_book_3():
    """
    create a new loan only if customer allowed and book is in library
    :return:
    """
    # get customer id and check if not punished
    customer_id = input('Enter customer_id: ')
    try:
        if customers_dict[customer_id].get_customer_status() != 'active':
            return print(f"{customer_id} is {customers_dict[customer_id].get_customer_status()}"
                         f", and can't loan books")
    except KeyError:
        return print(f'{customer_id} is not listed as customer')
    # get book num and check if in library
    try:
        book_num = int(input("Enter book_cat_number: "))
        if books_dict[book_num].get_book_status() != 'in library':
            return print('the book you asked is not in library')
        else:
            # add the new loan and change book status
            temp = Loan(customer_id, book_num, date.today().strftime('%d/%m/%Y'), books_dict[book_num].get_book_type())
            # line below is for checks(to enter other dates then today)
            # temp = Loan(customer_id, book_num, input('%d/%m/%Y: '), books_dict[book_num].get_book_type())
            loans_list.append(temp)
            books_dict[book_num].loan_book()
            save_data('books_dump.pkl', books_dict)
            save_data('loans_dump.pkl', loans_list)
            return print(f'customer {customer_id} loaned book {book_num}')
    except ValueError:
        return print('you did not enter a valid book catalog number')
    except KeyError:
        return print('the book number does not exist')


def return_book_4():
    # which book to return
    try:
        book_to_return = int(input('enter book number to return: '))
        # change loan status and book status
        for loan in loans_list:
            if book_to_return == loan.get_book_loaned() and loan.get_loan_status() != 'returned':
                books_dict[book_to_return].return_book()
                loan.return_book()
                save_data('books_dump.pkl', books_dict)
                save_data('loans_dump.pkl', loans_list)
                return print('book returned')
        return print(f'no open loans found for {book_to_return}')
    except ValueError:
        return print('you did not enter a valid book number')


def display_all_books_5():
    # print all books in the boos_dict
    for book in books_dict.values():
        print(book)
    print(f'there are {len(books_dict)} books')


def display_all_customers_6():
    # print all customers in customers_dict
    for customer in customers_dict.values():
        print(customer)
    return print(f'there are {len(customers_dict)} customers')


def display_all_loans_7():
    # print all loans in loans_dict
    for loan in loans_list:
        print(loan)
    return print(f'there are {len(loans_list)} loans')


def display_all_late_loans_8():
    # find and print all late loans
    late_count = 0
    for loan in loans_list:
        if loan.get_loan_status() == 'late':
            print(loan)
            late_count += 1
    return print(f'there are {late_count} late loans')


def display_loans_by_customer_9():
    """
    get a customer's id and display all the referred loans
    :return: a print of the relevant customers and all the relevant loans
    """
    look = input('enter customer id to display the relevant loans: ')
    try:
        print(customers_dict[look])
    except KeyError:
        return print('the id you are looking does not exist in our system')
    loans_count = 0
    for loan in loans_list:
        if loan.get_customer_loan() == look:
            print(loan)
            loans_count += 1
    return print(f'{look} has a total of {loans_count} loans')


def display_loans_by_book_10():
    """
    gets book name, creates a temporary list of books that match input name and the status(loaned)
    then print the relevant loans
    :return:
    """
    look = input('enter book name to display the relevant loans: ').lower()
    list_of_catnums = []
    # find all catalog numbers of loaned books with look name
    for book in books_dict.values():
        if book.get_book_name() == look and book.get_book_status() == 'loaned':
            list_of_catnums.append(book.get_cat_number())
    # print the relevant loan for every catalog number found
    for catnum in list_of_catnums:
        for loan in loans_list:
            if loan.get_book_loaned() == catnum:
                print(loan)
    return print(f'{len(list_of_catnums)} copies of {look} are loaned')


def find_book_by_name_11():
    """
    print all books with the same name as the input given
    :return: None
    """
    look = input('which book are you looking?: ').lower()
    copies = 0
    for book in books_dict.values():
        if book.get_book_name() == look:
            print(book)
            copies += 1
    return print(f'a total {copies} copies of {look} are listed')


def find_customer_by_name_12():
    """
    print all customers with the same name as the input given
    :return: None
    """
    for customer in customers_dict.values():
        if customer.get_customer_name() == input('enter a customer name to display: ').lower():
            print(customer)


def remove_book_13():
    """
    change book status to removed only if all copies status 'in library'
    :return: printed string with the relevant note
    """
    book_to_remove = input('which book you like to remove?: ')
    # make a list of books to check and remove
    ls_books = [book for book in books_dict.values() if book.get_book_name() == book_to_remove]
    if len(ls_books) == 0:
        return print('no books found')
    # if all copies of the book are in library remove all copies of the book else notify
    if {book.get_book_status() for book in ls_books} == {'in library'}:
        for book in ls_books:
            book.remove_book()
        save_data('books_dump.pkl', books_dict)
        return print(f'{book_to_remove} removed from library')
    else:
        return print(f'some copies are loaned, {book_to_remove} was not removed')


def remove_customer_14():
    """
    delete a customer from customer dictionary only if there are no open/late loans for the customer
    :return:
    """
    to_remove = input('enter customer id to remove: ')
    # check if customer has no open loanes
    for loan in loans_list:
        if loan.get_customer_loan() == to_remove:
            return print(f'customer {to_remove} did not return all the loaned books.\n'
                         f'{to_remove} was not removed')
    # if no open loans found, delete customer from dictionary
    customers_dict.pop(to_remove)
    save_data('customers_dump.pkl', customers_dict)
    return print(f'{to_remove} has been removed')


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
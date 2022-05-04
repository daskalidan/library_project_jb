import pickle


def load_data(file_name):
    with open(file_name, 'rb') as dump:
        return pickle.load(dump)


customers_dict = load_data('customers_dump.pkl')
books_dict = load_data('books_dump.pkl')
loans_list = load_data('loans_dump.pkl')

# use to format the saved files
# customers_dict = {}
# books_dict = {}
# loans_list = []


def save_data(file_name, dict_name):
    with open(file_name, 'wb') as dump:
        pickle.dump(dict_name, dump)


def main_menu():
    return print("""
    ---- welcome to library ----  
    0 - save & exit 
    1 - Add a new customer.
    2 - Add a new book.
    3 - Loan a book.
    4 - Return a book.
    5 - Display all books.
    6 - Display all customers.
    7 - Display all loans.
    8 - Display all late loans.
    9 - Display loans by customer.
    10 - Display loans by book.
    11 - Find a book by name.
    12 - Find a customer by name.
    13 - Remove book from library.
    14 - Remove customer. 
     """)


# from main_menu_funcs import *


if __name__ == '__main__':
    from customers import *
    from book import *
    from loans import *
    from main_menu_funcs import *

    # update late loans as of today
    open_loans = [loan for loan in loans_list if loan.get_loan_status() == 'open']
    for loan in open_loans:
        if loan.get_return_date() < date.today():
            loan.chang_to_late()
    save_data('loans_dump.pkl', loans_list)
    print('late loans updated')

    # update customer punish
    late_loans = [loan for loan in loans_list if loan.get_loan_status() == 'late']
    for lateloan in late_loans:
        customers_dict[lateloan.get_customer_loan()].punish()
    save_data('customers_dump.pkl', customers_dict)
    print('punish updated')

    # update customer unpunish
    punished = [customer for customer in customers_dict.values() if customer.get_customer_status() != 'active']
    for customer in punished:
        if date.today() > datetime.strptime(customer.get_customer_status()[15:25], '%d/%m/%Y').date():
            customer.unpunish()
    save_data('customers_dump.pkl', customers_dict)
    print('unpunish updated')

    print('all your data loaded and updated as of today')
    while True:
        input('press Enter to main menu: ')
        main_menu()
        choose_program(input('what would you like to do?: '))

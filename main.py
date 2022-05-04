import os


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


if __name__ == '__main__':

    from main_menu_funcs import *

    # update late loans as of today
    # update customer punish
    # update customer unpunish(if punish is over)
    # punished = [customer for customer in customers_dict.values(
    # ) if customer.get_customer_status() != 'active']
    # for customer in punished:
    #     if date.today() > datetime.strptime(customer.get_customer_status()[15:25], '%d/%m/%Y').date():
    #         customer.unpunish()

    while True:
        input('press Enter to main menu: ')
        os.system('cls')
        main_menu()
        choose_program(input('what would you like to do?: '))

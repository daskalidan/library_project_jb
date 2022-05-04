from datetime import *


class Loan:

    def __init__(self, customer_id, book_cat_number, loan_date, book_type):
        self._customer_loan = customer_id
        self._book_loaned = book_cat_number
        self._loan_date = datetime.strptime(loan_date, '%d/%m/%Y').date()
        self._return_date = \
            self._loan_date + timedelta({'1': 10, '2': 5, '3': 2}[book_type])
        self._loan_status = 'open'

    def __str__(self):
        return f'customer id: {self._customer_loan}, book catalog number: {self._book_loaned}, ' \
               f'loan date: {self._loan_date}, return date: {self._return_date}, status: {self._loan_status}.'

    def get_book_loaned(self):
        return self._book_loaned

    def return_book(self):
        self._loan_status = 'returned'

    def get_return_date(self):
        return self._return_date

    def get_customer_loan(self):
        return self._customer_loan

    def chang_to_late(self):
        self._loan_status = 'late'

    def get_loan_status(self):
        return self._loan_status

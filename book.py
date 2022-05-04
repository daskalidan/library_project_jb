

class Book:

    def __init__(self, book_name, author, book_type):
        with open('next_cat num.txt', 'r') as catr:
            next_cat_num = int(catr.read())
            self._cat_number = next_cat_num
            next_cat_num += 1
        with open('next_cat num.txt', 'w') as catw:
            catw.write(str(next_cat_num))
        self._book_name = book_name.lower()
        self._author = author.lower()
        self._book_type = book_type
        # book types: 1- up to 10 days loan
        #             2- up to 5 days loan
        #             3- up to 2 days loan
        # self._number_of_copies = None
        self._book_status = 'in library'

    def __str__(self):
        return f'catalog number: {self._cat_number}, book name: {self._book_name}, author: {self._author}, ' \
               f'book type: {self._book_type}, status: {self._book_status}.'

    def get_cat_number(self):
        return self._cat_number

    def get_book_name(self):
        return self._book_name

    def get_book_status(self):
        return self._book_status

    def get_book_type(self):
        return self._book_type

    def loan_book(self):
        self._book_status = 'loaned'

    def remove_book(self):
        self._book_status = 'removed'

    def return_book(self):
        self._book_status = 'in library'


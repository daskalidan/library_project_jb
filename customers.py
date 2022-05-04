from datetime import date, timedelta


class Customer:

    def __init__(self, id_number, name='unknown', city_address='unknown', age='unknown'):
        self._id_number = id_number
        self._name = name.lower()
        self._city_address = city_address.lower()
        self._age = age
        self._customer_status = 'active'

    def __str__(self):
        return f'ID: {self._id_number}, name: {self._name}, city: {self._city_address}, ' \
               f'age: {self._age}, status: {self._customer_status}.'

    def get_id_number(self):
        return self._id_number

    def get_customer_name(self):
        return self._name

    def get_customer_status(self):
        return self._customer_status

    def punish(self):
        until = date.today() + timedelta(14)
        self._customer_status = f"punished until {until.strftime('%d/%m/%Y')} if late loan is closed"

    def unpunish(self):
        self._customer_status = 'active'

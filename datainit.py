import sqlite3

def initialyze_database():
    con = sqlite3.connect('library_data.db')
    cur = con.cursor()
    try:
        cur.execute('DROP TABLE books')
    except:
        pass
    finally:
        cur.execute('''CREATE TABLE books
                    (cat_number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, book_name text, author text, book_type text, book_status text)''')
    
        init_books = [('the first book', 'me', '3', 'in library'), ('bible', 'GOD', '1', 'in library'), ('the first book', 'me', '3', 'in library'),
        ('bible', 'GOD', '1', 'in library'), ('bible', 'GOD', '1', 'in library'), ('bible', 'GOD', '1', 'in library'),
        ('harry poter', 'jk', '2', 'in library'), ('harry poter', 'jk', '2', 'in library'), ('harry poter', 'jk', '2', 'in library'), ('harry poter', 'jk', '2', 'in library')]
    
        for book in init_books:
            cur.execute(f'INSERT INTO books (book_name, author, book_type, book_status) VALUES {book}')
        con.commit()    

    try:
        cur.execute('DROP TABLE customers')
    except:
        pass
    finally:
        cur.execute('''CREATE TABLE customers
                    (id_number text NOT NULL PRIMARY KEY, name text, city_address text, age text, customer_status text)''')

        init_customers = [('000000001', 'adam', 'heven', '100000', 'active'), ('000000002', 'eve', 'heven', '100000', 'active'), ('000000011', 'avi', 'sadom', '30000', 'active'), 
        ('000002341', 'gever', 'tel aviv', '33', 'active'), ('000562341', 'yosi', 'natanya', '22', 'active'), ('111111111', 'me', 'here', '16', 'active')]

        for customer in init_customers:
            cur.execute(f'INSERT INTO customers (id_number, name, city_address, age, customer_status) VALUES {customer}')
        con.commit()    

    try:
        cur.execute('DROP TABLE loans')
    except:
        pass    
    finally:
        cur.execute('''CREATE TABLE loans
                        (id_number text,
                        cat_number int,
                        loan_date text,
                        date_to_return text, 
                        loan_status text,
                        FOREIGN KEY (id_number) REFERENCES customers(id_number),
                        FOREIGN KEY (cat_number) REFERENCES books(cat_number)
                        )''')
    for row in cur.execute('SELECT * FROM books'):
            print(row) 
    for row in cur.execute('SELECT * FROM customers'):
            print(row)                             
    con.close()

if __name__ == '__main__':
    initialyze_database()
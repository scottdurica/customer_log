import sqlite3


class DBHandler():

    def __init__(self):
        self.conn = sqlite3.connect('customer_tracker.db')
        self.cur = self.conn.cursor()
        self.table_init()

    def table_init(self):
        # Do some setup
        self.cur.executescript('''

        CREATE TABLE IF NOT EXISTS customer (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name   TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS contact (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            address  TEXT,
            email TEXT,
            phone TEXT,
            mailing_list INTEGER,
            customer_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS invoice (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            description TEXT,
            customer_id INTEGER
        )
        ''')

    def get_id_from_cus_name(self, name):
        self.cur.execute(
            "SELECT id FROM customer WHERE name=?", (name,))
        return self.cur.fetchone()[0]

    def fetch_customers(self):
        # self.cur.execute("SELECT * FROM customer")
        self.cur.execute('''SELECT name, phone, email FROM customer
                        JOIN contact ON customer.id = contact.customer_id''')
        return self.cur.fetchall()

    def fetch_customer_by_id(self, id):
        self.cur.execute("SELECT name FROM customer WHERE id=?", (id,))
        return self.cur.fetchone()

    def fetch_customer_by_name(self, name):
        self.cur.execute(
            "SELECT id FROM customer WHERE name=?", (name,))
        id = self.cur.fetchone()[0]
        self.cur.execute('''SELECT email, phone, address, mailing_list
                         FROM contact WHERE customer_id=?''', (id,))
        return self.cur.fetchone()

    def fetch_customer_name_for_invoice(self, invoice_number):
        self.cur.execute('''SELECT name FROM customer
                        JOIN invoice ON customer.id = invoice.customer_id WHERE invoice.invoice_number=?''', (invoice_number,))
        return self.cur.fetchone()

    def fetch_invoices_for_name(self, name):
        self.cur.execute("SELECT id FROM customer WHERE name=?", (name,))
        id = self.cur.fetchone()[0]
        self.cur.execute(
            "SELECT invoice_number, description FROM invoice WHERE customer_id=?", (id,))
        return self.cur.fetchall()

    def fetch_invoice_by_number(self, invoice_number):
        self.cur.execute(
            "SELECT description FROM invoice WHERE invoice_number=?", (invoice_number,))
        return self.cur.fetchone()[0]

    def add_customer(self, name, address, email, phone, mailing_list):
        # first, check for and add if not there the customer to db
        self.cur.execute('''INSERT OR IGNORE INTO customer (name)
            VALUES(?)''', (name,))
        if self.cur.rowcount != 1:
            print('Error saving new customer to DB')
            return
        else:
            # retrieve the generated id to pass into the contact table
            customer_id = self.cur.lastrowid
            # customer was saved - and not IGNORED, which means
            row = self.fetch_customer_by_id(customer_id)
            # print('row is: ', row)

            # then add the rest of the data to the contact table
            self.cur.execute('''INSERT INTO contact (address, email, phone, mailing_list, customer_id)
                VALUES(?,?,?,?,?)''', (address, email, phone, mailing_list, customer_id))
            if self.cur.rowcount != 1:
                print('Error saving new customer contact information to DB')
                return
            else:
                self.conn.commit()
                return row

    def add_invoice(self, name, invoice_number, description):
            # first, get the customer's id from customer table
        id = self.get_id_from_cus_name(name)
        # print('id val is: ', id)
        # print(f'ID: {id}  INV: {invoice_number}  DESC: {description}')
        self.cur.execute('''INSERT OR IGNORE INTO invoice (invoice_number, description, customer_id)
                VALUES(?,?,?)''', (invoice_number, description, id))
        if self.cur.rowcount != 1:
            print('Error saving new invoice to DB')
            return
        else:
            self.conn.commit()

    def delete_invoice(self, invoice_number):
        self.cur.execute(
            "DELETE FROM invoice WHERE invoice_number=?", (invoice_number,))
        self.conn.commit()

    def delete_customer(self, name):
        self.cur.execute("SELECT id FROM customer WHERE name=?", (name,))
        id = self.cur.fetchone()[0]
        self.cur.execute('''DELETE FROM contact WHERE customer_id=?''', (id,))
        self.cur.execute("DELETE FROM customer WHERE name=?", (name,))
        self.conn.commit()

    def update_customer(self, old_name, name, address, email, phone, mailing_list):
        self.cur.execute("SELECT id FROM customer WHERE name=?", (old_name,))
        id = self.cur.fetchone()[0]
        self.cur.execute('''UPDATE contact SET address=?, email=?, phone=?, mailing_list=?
                            WHERE customer_id=?''', (address, email, phone, mailing_list, id))
        self.cur.execute("UPDATE customer SET name=? WHERE id=?", (name, id))
        self.conn.commit()

    def update_invoice(self, old_name, invoice_number, description):
        self.cur.execute('''UPDATE OR IGNORE invoice SET invoice_number=?, description=?
                            WHERE invoice_number=?''', (invoice_number, description, old_name))
        if self.cur.rowcount != 1:
            print('Error updating invoice- Invalid invoice number??')
            return
        else:
            self.conn.commit()
    # get weather desxription and icon name using the weather_id--return dict

    # def get_icon_from_weatherid(self, weather_id):
    #     self.cur.execute('''SELECT icon_id, description FROM conditions
    #     WHERE id=?''', (weather_id,))

    #     self.conn.commit()
    #     val = self.cur.fetchone()
    #     desc = val[1]

    #     self.cur.execute('''SELECT name FROM icons
    #     WHERE id=?''', (val[0],))

    #     self.conn.commit()
    #     val = self.cur.fetchone()
    #     i_name = val[0]
    #     # reuturn dict
    #     values = {'icon': i_name, 'description': desc}

    #     return values

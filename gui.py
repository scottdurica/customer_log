import tkinter as tk
from enum import Enum
import tkinter.font as TkFont
from tkinter import ttk
from tkinter import *
import validate
from ttkthemes import ThemedTk

# window = ThemedTk(theme="arc")

# bg_color = '#32a4a8'
# text_color = '#fff'
# text_big = 42
# text_med = 28
# text_small = 18

# > import ttk
# >>> s=ttk.Style()
# >>> s.theme_names()
# ('clam', 'alt', 'default', 'classic')

class GUI(tk.Tk):

    def __init__(self, db):
        tk.Tk.__init__(self)
        root = self
        # root = ThemedTk(theme='radiance')
        root.title("Customer Logs")
        self.db = db
        # keep track of current tab to autofill field data across tabs
        self.current_tab = 0
        # style = ttk.Style()
        # print(style.theme_names())
        # style.theme_use('alt')
        # print(style.theme_use())
        self.container = ttk.Notebook(
            root, height=400, width=740)
        self.container.bind('<<NotebookTabChanged>>', self.tab_change_event)
        self.customer_tab = ttk.Frame(self.container, padding=20)
        emails_tab = ttk.Frame(self.container, padding=20)
        invoices_tab = ttk.Frame(self.container, padding=20)

        self.container.add(self.customer_tab, text='Customers')
        self.container.add(emails_tab, text='Emails')
        self.container.add(invoices_tab, text='Invoices')

        self.container.pack(expand=1, fill='both')

        self.ct = CusTab(db, self.customer_tab)
        self.it = InvTab(db, invoices_tab)

    def tab_change_event(self, event):
        # Invoice tab was selected-
        if self.container.index(self.container.select()) == 2:
            # clear the combobox field in case that entry was deleted from DB in another tab
            self.it.clear_visual_data()

            if self.current_tab == 0:
                # coming here from the customer tab pass current value in name
                # field (if any) to preload into invoice fields
                if not self.ct.selected_item == None:
                    self.it.preload_customer(self.ct.selected_item)
            self.current_tab = 0
        # Customer tab was selected-
        elif self.container.index(self.container.select()) == 0:
            self.current_tab = 0
        # Email tab was selected-
        elif self.container.index(self.container.select()) == 1:
            self.current_tab = 1


class CusTab():

    def __init__(self, db, container):
        self.db = db
        # self.root = root
        # self.tab_control = ttk.Notebook(self.root, height=400, width=740)
        self.populate_tabs(container)
        self.populate_list_view()
        self.selected_item = None
        self.validated_field_values = {}

    def populate_list_view(self):
        self.list_box.delete(0, END)
        customer_list = self.db.fetch_customers()
        customer_list.sort()
        for item in customer_list:
            self.list_box.insert(END, item[0])

    def validate_fields(self):
        if validate.v_name(self.f_name.get(), self.l_name.get()):
            name = validate.f_name(self.f_name.get(), self.l_name.get())
        else:
            return False
        if validate.v_email(self.email.get()):
            email = validate.f_email(self.email.get())
        else:
            return False
        if validate.v_phone(self.phone.get()):
            phone = validate.f_phone(self.phone.get())
        else:
            return False
        if validate.v_address(self.address.get()):
            address = validate.f_address(self.address.get())
        else:
            return False
        mail_list = self.mail_list_check.get()
        self.validated_field_values = {
            'name': name, 'email': email, 'phone': phone, 'address': address, 'mail_list': mail_list}

        # print(self.validated_field_values)
        return True

    def add_customer(self):
        if self.validate_fields():
            # save to database
            self.db.add_customer(self.validated_field_values['name'], self.validated_field_values['address'],
                                 self.validated_field_values['email'], self.validated_field_values['phone'], self.validated_field_values['mail_list'])
            self.populate_list_view()
            self.clear_fields()

    def clear_fields(self):
        self.selected_item = None
        self.delete_entries()

    def edit_customer(self):
        if self.selected_item == None or self.selected_item == '':
            return
        else:
            old_name = self.selected_item
            if self.validate_fields():
                self.db.update_customer(
                    old_name, self.validated_field_values['name'], self.validated_field_values['address'],
                    self.validated_field_values['email'], self.validated_field_values['phone'], self.validated_field_values['mail_list'])
                self.delete_entries()
                self.populate_list_view()

    def remove_customer(self):
        if self.selected_item == None or self.selected_item == '':
            return
        else:
            self.db.delete_customer(self.selected_item)
            self.delete_entries()
            self.populate_list_view()

    def select_listview_item(self, event):
        # get selection in list_view
        index = self.list_box.curselection()
        self.selected_item = self.list_box.get(index)
        # populate entry fields with selected row
        self.delete_entries()
        customer_list = self.db.fetch_customer_by_name(self.selected_item)
        # customer list val:  ('wdbv@xmail.com', '4432345467', 'That Road ', 0)
        lf = self.selected_item.split(',')
        f = lf[1].strip()
        l = lf[0].strip()
        self.f_name.insert(0, f)
        self.l_name.insert(0, l)
        self.email.insert(0, customer_list[0])
        self.phone.insert(0, customer_list[1])
        self.address.insert(0, customer_list[2])
        self.mail_list_check.set(customer_list[3])

    # clear the entry fields
    def delete_entries(self):
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.address.delete(0, END)
        self.mail_list_check.set(0)

    def populate_tabs(self, customer_tab):
        f_name = StringVar()
        l_name = StringVar()
        email = StringVar()
        phone = StringVar()
        address = StringVar()
        self.mail_list_check = IntVar()

        # Populate the customer tab
        ttk.Label(customer_tab, text='First Name:').grid(
            sticky='w', column=0, row=0, padx=20, pady=10)
        ttk.Label(customer_tab, text='Last Name:').grid(
            sticky='w', column=0, row=1, padx=20, pady=10)
        ttk.Label(customer_tab, text='Email:').grid(
            sticky='w', column=0, row=2, padx=20, pady=10)
        ttk.Label(customer_tab, text='Phone:').grid(
            sticky='w', column=0, row=3, padx=20, pady=10)
        ttk.Label(customer_tab, text='Address:').grid(
            sticky='w', column=0, row=4, padx=20, pady=10)
        self.mail_list_cb = ttk.Checkbutton(
            customer_tab, text='Add to mailing list?', variable=self.mail_list_check)
        self.mail_list_cb.grid(column=1, row=5, padx=5, pady=10, sticky='e')

        # Customer imput items
        self.f_name = ttk.Entry(customer_tab, textvariable=f_name)
        self.f_name.grid(column=1, row=0)
        self.l_name = ttk.Entry(customer_tab, textvariable=l_name)
        self.l_name.grid(column=1, row=1)
        self.email = ttk.Entry(customer_tab, textvariable=email)
        self.email.grid(column=1, row=2)
        self.phone = ttk.Entry(customer_tab, textvariable=phone)
        self.phone.grid(column=1, row=3)
        self.address = ttk.Entry(customer_tab, textvariable=address)
        self.address.grid(column=1, row=4)

        ttk.Separator(customer_tab, orient='vertical').grid(
            column=2, row=0, rowspan=6, sticky='ns', padx=10)

        #  Create scrollbar and listbox
        self.list_box = Listbox(customer_tab, height=12, width=40, border=0)
        self.list_box.grid(row=0, column=4, rowspan=6)
        scrollbar = Scrollbar(customer_tab)
        scrollbar.grid(row=0, column=5, rowspan=6)
        # Hook up scrollbar to listview
        self.list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.list_box.yview)
        # bind select method
        self.list_box.bind('<<ListboxSelect>>', self.select_listview_item)

        # Create buttons
        btn_bar = ttk.Frame(customer_tab, padding=20)
        btn_bar.grid(row=6, column=0, columnspan=5)

        add_btn = ttk.Button(btn_bar, text='Add Customer',
                             width=12, command=self.add_customer)
        add_btn.grid(row=5, column=0, pady=35, padx=10)

        edit_btn = ttk.Button(btn_bar, text='Edit Customer',
                              width=12, command=self.edit_customer)
        edit_btn.grid(row=5, column=1, pady=35, padx=10)

        remove_btn = ttk.Button(btn_bar, text='Remove Customer',
                                width=15, command=self.remove_customer)
        remove_btn.grid(row=5, column=2, pady=35, padx=10)

        clear_btn = ttk.Button(btn_bar, text='Clear Form',
                               width=12, command=self.clear_fields)
        clear_btn.grid(row=5, column=3, pady=35, padx=10)


class InvTab():
    pass

    def __init__(self, db, container):
        self.db = db
        self.dropdwn_list = []
        self.name_field = None
        self.populate_tabs(container)
        self.validated_values = {}
        self.selected_item = None

    def refresh_customer_data(self):
        pass

    def select_listview_item(self, event):
        # # get selection in list_view
        index = self.list_box.curselection()  # returns tuple
        # do nothing unless actual invoice is selected
        if index[0] > 1:
            self.selected_item = self.list_box.get(index)
            # # populate entry fields with selected row
            # self.delete_entries()
            self.clear_inv_and_desc()
            i_desc = self.db.fetch_invoice_by_number(self.selected_item)
            self.inv_num.insert(0, self.selected_item)
            self.desc.insert(0, i_desc)

    def clear_visual_data(self):
        if self.name_field != None:
            self.name_field.set('')
        self.dropdwn_list.clear()
        self.list_box.delete(0, END)

    ### this loads the combobox dropdown with customer names...called from postcommand ###
    def populate_dd_cust_list(self):
        self.dropdwn_list.clear()
        data = self.db.fetch_customers()
        for row in data:
            self.dropdwn_list.append(row[0])
        self.dropdwn_list.sort()
        self.name_field['values'] = self.dropdwn_list

    def populate_list_view(self, name):
        self.list_box.delete(0, END)
        invoice_list = self.db.fetch_invoices_for_name(name)
        self.list_box.insert(0, name)
        if len(invoice_list) == 0:
            self.list_box.insert(
                END, 'No Invoices associated with this customer')
        else:
            self.list_box.insert(END, 'Invoices for this customer:')
        for item in invoice_list:
            self.list_box.insert(END, item[0])

    # this gets called as user selects a value from the combobox ###

    def select_combobox_item(self, event):
        name = (self.name_field.get())
        # use name value to popluate the listview with the correct data from DB
        self.populate_list_view(name)
        self.clear_inv_and_desc()

    def clear_inv_and_desc(self):
        self.inv_num.delete(0, END)
        self.desc.delete(0, END)
    # Gets called from the GUI class

    def preload_customer(self, name):
        self.dropdwn_list.clear()
        data = self.db.fetch_customers()
        for row in data:
            self.dropdwn_list.append(row[0])
        self.dropdwn_list.sort()
        self.name_field['values'] = self.dropdwn_list
        for i in self.dropdwn_list:
            if i == name:
                self.name_field.current(self.dropdwn_list.index(i))
                break
        self.populate_list_view(name)

    def validate_fields(self):
        if validate.str_larger(self.name_field.get(), 2):
            name = self.name_field.get()
        else:
            return False
        if validate.str_larger(self.inv_num.get(), 1):
            i_num = validate.strip_and_cap(self.inv_num.get())
        else:
            return False
        if validate.str_larger(self.desc.get(), 0):
            descrip = self.desc.get()
        else:
            return False
        self.validated_values.clear()
        self.validated_values = {
            'name': name, 'invoice_number': i_num, 'description': descrip}
        return True

    def add_invoice(self):
        if self.validate_fields():
            # save to database
            self.db.add_invoice(
                self.validated_values['name'], self.validated_values['invoice_number'], self.validated_values['description'])
            self.populate_list_view(self.validated_values['name'])
            self.clear_inv_and_desc()

    def edit_invoice(self):
        if not self.selected_item == None:
            old_inv_num = self.selected_item
            if self.validate_fields():
                self.db.update_invoice(
                    old_inv_num, self.validated_values['invoice_number'], self.validated_values['description'])

    def remove_invoice(self):
        if not self.selected_item == None:
            # get name of customer that owns this invoice
            i_num = self.db.fetch_customer_name_for_invoice(self.selected_item)
            # print('returned value for cus name; ', i_num[0])
            self.db.delete_invoice(self.selected_item)
            # empty the fields
            self.inv_num.delete(0, END)
            self.desc.delete(0, END)
            # get current customer and repopulate the list
            self.selected_item = None
            self.populate_list_view(i_num[0])

    def clear_fields(self):
        self.clear_visual_data()
        self.clear_inv_and_desc()

    def populate_tabs(self, container):
        c_name = StringVar()
        i_num = IntVar()
        desc_val = StringVar()
        # self.populate_dd_cust_list()

        # Populate the invoice tab
        ttk.Label(container, text='Customer name:').grid(
            sticky='w', column=0, row=0, padx=20, pady=10)
        self.name_field = ttk.Combobox(
            container, textvariable=c_name, postcommand=self.populate_dd_cust_list)
        self.name_field.grid(column=1, row=0, padx=20, pady=10)
        ttk.Label(container, text='Invoice Number:').grid(
            sticky='w', column=0, row=1, padx=20, pady=10)
        ttk.Label(container, text='Description:').grid(
            sticky='w', column=0, row=2, padx=20, pady=10)
        # bind combobox selected item event
        self.name_field.bind('<<ComboboxSelected>>', self.select_combobox_item)

        # invoice imput items
        self.inv_num = ttk.Entry(container, textvariable=i_num)
        self.inv_num.grid(column=1, row=1)
        self.desc = ttk.Entry(container, textvariable=desc_val)
        self.desc.grid(column=1, row=2)

        ttk.Separator(container, orient='vertical').grid(
            column=2, row=0, rowspan=6, sticky='ns', padx=10)

        #  Create scrollbar and listbox
        self.list_box = Listbox(container, height=12, width=40, border=0)
        self.list_box.grid(row=0, column=4, rowspan=6)
        scrollbar = Scrollbar(container)
        scrollbar.grid(row=0, column=5, rowspan=6)
        # Hook up scrollbar to listview
        self.list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.list_box.yview)
        # bind select method
        self.list_box.bind('<<ListboxSelect>>', self.select_listview_item)

        # Create buttons
        btn_bar = ttk.Frame(container, padding=20)
        btn_bar.grid(row=6, column=0, columnspan=5)

        add_btn = ttk.Button(btn_bar, text='Add Invoice',
                             width=12, command=self.add_invoice)
        add_btn.grid(row=5, column=0, pady=35, padx=10)

        edit_btn = ttk.Button(btn_bar, text='Edit Invoice',
                              width=12, command=self.edit_invoice)
        edit_btn.grid(row=5, column=1, pady=35, padx=10)

        remove_btn = ttk.Button(btn_bar, text='Remove Invoice',
                                width=15, command=self.remove_invoice)
        remove_btn.grid(row=5, column=2, pady=35, padx=10)

        clear_btn = ttk.Button(btn_bar, text='Clear Form',
                               width=12, command=self.clear_fields)
        clear_btn.grid(row=5, column=3, pady=35, padx=10)

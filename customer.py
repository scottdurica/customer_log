from datetime import date


class Customer:

    def __init__(self, f_name, l_name, email, phone):
        self.first_name = f_name
        self.last_name = l_name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f'Customer name: {self.first_name} {self.last_name} Email: {self.email} Phone: {self.phone}'


scott = Customer('Scott', 'Durica', 'scottd@g.com', '6037154704')
suzanne = Customer('Suzanne', 'Resendes', 'suzzied@g.com', '6032030782')

print(scott)
print(suzanne)

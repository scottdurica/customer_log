import re

# regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
regex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def empty_str(str, len_arg):
    return len(str.strip()) < len_arg


def str_larger(str, len_arg):
    return len(str.strip()) > len_arg


def strip_and_cap(str):
    return str.strip().capitalize()


def v_name(f, l):
    if empty_str(f, 1):
        print('invalid first name field')
        return False
    if empty_str(l, 3):
        print('invalid last name field')
        return False
    return True


def f_name(f, l):
    return f'{l.capitalize()}, {f.capitalize()}'


def v_email(email):
    if(re.search(regex_email, email)):
        return True
    # raise Exception('Email not formatted correctly')


def f_email(email):
    return email.strip()


def v_phone(str):
    num = ''
    if len(str) > 0:
        for ch in str:
            if ch.isdigit():
                num += ch
    if len(num) == 10:
        return True
    print('phone number not valid')
    return False


def f_phone(str):
    num = ''
    if len(str) > 0:
        for ch in str:
            if ch.isdigit():
                num += ch
    return num


def v_address(address):
    if empty_str(address, 3):
        print('address field is too short')
        return False
    return True


def f_address(address):
    f_address = ''
    words = address.split()
    for word in words:
        f_address += f'{word.strip().capitalize()} '
    if f_address.endswith(','):
        add_copy = f_address[:-1]
        return add_copy
    else:
        return f_address

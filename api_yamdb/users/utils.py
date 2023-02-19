import string
from random import sample

LENGTH = 20


def generate_confirmation_code():
    letters_and_digits = string.ascii_letters + string.digits
    confirmation_code = ''.join(sample(letters_and_digits, LENGTH))
    return confirmation_code

import random
import string

def generate_password(length=12, use_digits=True, use_specials=True, use_upper=True):
    chars = string.ascii_letters
    chars = list(string.ascii_lowercase)
    if use_digits:
        chars += string.digits
    if use_specials:
        chars += list("!@#$%^&*_-+=")
    if use_upper:
        chars += string.ascii_uppercase

    if not chars:
        chars = string.ascii_letters  # Fallback, falls alle Häkchen weg
    return ''.join(random.choice(chars) for _ in range(length))
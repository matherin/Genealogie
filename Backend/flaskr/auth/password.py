import hashlib
import random

_PASSWORD_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*?"
_PASSWORD_LENGTH = 12
def generate_user_password():
    return ''.join(random.choice(_PASSWORD_CHARSET) for i in range(_PASSWORD_LENGTH)) 

def get_hash(pw):
    return hashlib.sha512(pw.encode('utf-8')).hexdigest()

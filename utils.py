from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)

def verify_password(hashed_password, user_password):
    return ph.verify(hashed_password, user_password)
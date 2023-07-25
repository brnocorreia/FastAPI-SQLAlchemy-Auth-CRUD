from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, hash_password: str) -> bool:
    """
    Function to verify if the password is correct, comparing the password passed by user and her hashed-one
    which is storaged in the database.
    """
    return CRYPTO.verify(password, hash_password)


def hash_generator(password: str) -> str:
    """
    Function to generate and return the hash password
    """
    return CRYPTO.hash(password)

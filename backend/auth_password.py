from argon2 import PasswordHasher


def get_hashed_password(plain_password: str) -> str:
    return PasswordHasher().hash(plain_password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        return PasswordHasher().verify(hashed_password, plain_password)
    except:
        raise ValueError("Incorrect password")

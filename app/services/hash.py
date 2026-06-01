import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    )

    return hashed.decode("utf-8")

def verify_password(passwordEntered:str,password:str)->bool:
    is_valid=bcrypt.checkpw(
        passwordEntered.encode("utf-8"),
        password.encode("utf-8")
    )
    return is_valid
import os
from fastapi import HTTPException, status

ADMIN_SECRET = os.getenv("secret_key")


def check_admin_key(admin_key: str):

    if admin_key != ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin key"
        )
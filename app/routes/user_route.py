from fastapi import APIRouter, HTTPException, status
import os
from database.db import db
from schemas.user_schema import (
    UserSignup,
    UserSignin,
    UserResponse,
)
from services.hash import hash_password, verify_password
userRouter = APIRouter()

@userRouter.post(
    "/signup",
    response_model=UserResponse
)
async def signup(user_data: UserSignup):

    existing_email = await db.users.find_one(
        {"email": user_data.email}
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(
            user_data.password
        ),
        "is_admin": False,
        "manager_id": None
    }
    result = await db.users.insert_one(
        new_user
    )

    return UserResponse(
        id=result._id,
        username=user_data.username,
        email=user_data.email,
        isAdmin= False
    )

@userRouter.post("/signin")
async def signin(user_data: UserSignin):

    user = await db.users.find_one(
        {"email": user_data.email}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            isAdmin=user['is_admin']
        )
    }

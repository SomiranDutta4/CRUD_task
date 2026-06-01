from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
import os

from database.db import db
from schemas.user_schema import (
    UserResponse
)
from schemas.admin_schema import (
    AdminSignUp,
    ManagerUpdateSchema,
    AdminSignin
)
from services.hash import (
    hash_password,
    verify_password
)
from services.checkAdmin import check_admin_key

adminRoute = APIRouter()

ADMIN_SECRET = os.getenv("secret_key")


@adminRoute.post("/signup")
async def admin_signup(user_data: AdminSignUp):

    check_admin_key(user_data.admin_key)

    existing_email = await db.users.find_one(
        {
            "email": user_data.email
        }
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_admin = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(
            user_data.password
        ),
        "is_admin": True,
        "manager_id": None
    }

    result = await db.users.insert_one(
        new_admin
    )

    created_admin = await db.users.find_one(
        {
            "_id": result.inserted_id
        }
    )

    return {
        "message": "Admin created successfully",
        "admin": {
            "id": str(created_admin["_id"]),
            "username": created_admin["username"],
            "email": created_admin["email"],
            "isAdmin": True
        }
    }


@adminRoute.post("/signin")
async def admin_signin(
    user_data: AdminSignin
):
    
    check_admin_key(user_data.admin_key)

    user = await db.users.find_one(
        {
            "email": user_data.email
        }
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

    if not user.get(
        "is_admin",
        False
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return {
        "message": "Admin login successful",
        "user": UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            isAdmin=True
        )
    }


@adminRoute.put("/manager/update")
async def update_manager(
    data: ManagerUpdateSchema,
    admin_id: str
):

    try:
        admin = await db.users.find_one(
            {
                "_id": ObjectId(admin_id)
            }
        )
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid admin id"
        )

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    if not admin.get(
        "is_admin",
        False
    ):
        raise HTTPException(
            status_code=403,
            detail="Only admins can assign managers"
        )

    if data.employee_id == data.manager_id:
        raise HTTPException(
            status_code=400,
            detail="Employee cannot be their own manager"
        )

    employee = await db.users.find_one(
        {
            "_id": ObjectId(
                data.employee_id
            )
        }
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    manager = await db.users.find_one(
        {
            "_id": ObjectId(
                data.manager_id
            )
        }
    )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found"
        )

    await db.users.update_one(
        {
            "_id": ObjectId(
                data.employee_id
            )
        },
        {
            "$set": {
                "manager_id": data.manager_id
            }
        }
    )

    return {
        "message": "Manager updated successfully",
        "employee_id": data.employee_id,
        "manager_id": data.manager_id
    }
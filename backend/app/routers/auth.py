from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from datetime import timedelta
from ..utils.auth import create_access_token

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/token", tags=["Auth"])
async def login_for_access_token(user: UserLogin) -> Dict[str, str]:
    # Mock user authentication - Replace with actual DB check
    if user.username == "testuser" and user.password == "password":
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

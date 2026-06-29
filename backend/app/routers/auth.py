from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.db import USERS
from app.auth_utils import create_token, get_current_user
from passlib.context import CryptContext

router = APIRouter()
pwd    = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginOut(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    initials: str
    role: str
    employee_id: int


@router.post("/login", response_model=LoginOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in USERS if u["username"] == form.username), None)
    if not user or not pwd.verify(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user["id"]})
    return LoginOut(
        access_token=token, token_type="bearer",
        user_id=user["id"], name=user["name"],
        initials=user["initials"], role=user["role"],
        employee_id=user["employee_id"],
    )


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {k: v for k, v in user.items() if k != "hashed_password"}
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.database.session import get_db
from app.auth.security import create_access_token, create_refresh_token, verify_password, get_password_hash, decode_token
from app.auth.dependencies import get_current_user
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.schemas.user import UserCreate, UserResponse, Token, PasswordReset, PasswordResetConfirm, ChangePassword
from app.config import settings

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await UserService.create(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login(credentials: dict, db: AsyncSession = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    user = await UserService.authenticate(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.user_id)})
    refresh_token = create_refresh_token({"sub": str(user.user_id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: dict):
    token = token_data.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="Refresh token required")
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload.get("sub")
    access_token = create_access_token({"sub": user_id})
    refresh_token = create_refresh_token({"sub": user_id})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password")
async def forgot_password(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_by_email(db, data.email)
    if user:
        token = create_access_token({"sub": str(user.user_id)}, expires_delta=timedelta(hours=1))
        await EmailService.send_password_reset_email(data.email, token)
    return {"message": "If an account exists, a password reset email has been sent"}

@router.post("/reset-password")
async def reset_password(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    payload = decode_token(data.token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user_id = int(payload.get("sub"))
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = get_password_hash(data.new_password)
    await db.commit()
    return {"message": "Password reset successfully"}

@router.post("/change-password")
async def change_password(data: ChangePassword, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    success = await UserService.change_password(db, current_user.user_id, data.current_password, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    return {"message": "Password changed successfully"}

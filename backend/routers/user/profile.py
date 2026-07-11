from fastapi import APIRouter, Depends, UploadFile, File, Form

from models.user import User
from utils.auth import get_current_user
from services.user.profile_service import ProfileService
from config.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    crop_x: int = Form(0),
    crop_y: int = Form(0),
    crop_w: int = Form(0),
    crop_h: int = Form(0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProfileService(db)
    return service.upload_avatar(
        current_user,
        await file.read(),
        file.filename or "avatar.png",
        crop_x, crop_y, crop_w, crop_h,
    )


@router.put("/profile")
async def update_profile(
    username: str = Form(...),
    email: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProfileService(db)
    return service.update_profile(current_user, username, email)

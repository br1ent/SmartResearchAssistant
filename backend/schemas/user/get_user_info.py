from datetime import datetime

from pydantic import BaseModel


class GetUserInfoOut(BaseModel):
    id: int
    username: str
    email: str
    photo: str
    create_at: datetime | None = None
    update_at: datetime | None = None

    model_config = {"from_attributes": True}
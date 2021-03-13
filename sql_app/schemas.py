from pydantic.main import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True

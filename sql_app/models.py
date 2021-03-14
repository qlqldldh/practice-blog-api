from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sql_app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, default="")
    created_at = Column(DateTime, default=datetime.today())

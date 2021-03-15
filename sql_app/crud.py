from sql_app import models
from sql_app.database import Session
from sql_app.schemas import PostCreate, Post
from sql_app.utils import get_dict_from_model


def create_post(db: Session, post: PostCreate):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id)
    return None if db_post.count() > 1 else db_post.first()


def get_post_list(db: Session):
    return db.query(models.Post).all()


def update_post(db: Session, post: Post):
    db_post = db.query(models.Post).get(post.id)
    post_dict = get_dict_from_model(post)
    for key, value in post_dict.items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)

    return db_post

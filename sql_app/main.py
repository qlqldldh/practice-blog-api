from fastapi import FastAPI, Depends, status

from sql_app import models, schemas, crud
from sql_app.database import engine, Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def new_post(title: str, content: str, db: Session = Depends(get_db)):
    post = schemas.PostCreate(title=title, content=content)

    return crud.create_post(db, post)


@app.get("/posts/", status_code=status.HTTP_200_OK)
def post_list(db: Session = Depends(get_db)):
    return crud.get_post_list(db)


@app.get("/posts/{post_id}")
def post_detail(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id)

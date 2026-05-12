from sqlalchemy.orm import Session
from . import models, schemas, auth

# ── User Operations ───────────────────────
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ── Task Operations ───────────────────────
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()


def update_task(db: Session, task_id: int, user_id: int, updates: schemas.TaskUpdate):
    task = get_task(db, task_id, user_id)
    if not task:
        return None
    for key, val in updates.dict(exclude_unset=True).items():
        setattr(task, key, val)
        db.commit()
        db.refresh(task)
        return task
    

def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
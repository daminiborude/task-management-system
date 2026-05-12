from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, schemas, auth, models
from .database import engine, Base
from .dependencies import get_db, get_current_user


# Create all tables on startup
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task Manager API")


# ── Auth Endpoints ────────────────────────
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session =Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form.username)
    if not user or not auth.verify_password(form.password,user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# ── Task Endpoints ────────────────────────
@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return crud.create_task(db, task, current_user.id)


@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return crud.get_tasks(db, current_user.id)


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int,updates: schemas.TaskUpdate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    task = crud.update_task(db, task_id, current_user.id,updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    if not crud.delete_task(db, task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


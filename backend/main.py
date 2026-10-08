import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Variable de entorno solicitada
ENTORNO = os.getenv("ENTORNO", "Entorno no configurado")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://user:password@db:3306/appdb",
)

engine = None
for _ in range(10):
  try:
    engine = create_engine(DATABASE_URL)
    engine.connect()
    break
  except Exception:
    time.sleep(2)

Base = declarative_base()


class Task(Base):
  __tablename__ = "tasks"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(255), nullable=False)


if engine:
  Base.metadata.create_all(bind=engine)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
  title: str


# Nuevo endpoint para consultar el entorno
@app.get("/api/entorno")
def get_entorno():
  return {"entorno": ENTORNO}


@app.get("/api/tasks")
def get_tasks():
  db = SessionLocal()
  tasks = db.query(Task).all()
  db.close()
  return tasks


@app.post("/api/tasks")
def create_task(task: TaskCreate):
  db = SessionLocal()
  db_task = Task(title=task.title)
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  db.close()
  return db_task
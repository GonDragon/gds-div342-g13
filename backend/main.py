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


class User(Base):
  __tablename__ = "usuarios"
  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(255), nullable=False)


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


class UserCreate(BaseModel):
  nombre: str


# Nuevo endpoint para consultar el entorno
@app.get("/api/entorno")
def get_entorno():
  return {"entorno": ENTORNO}


@app.get("/api/usuarios")
def get_users():
  db = SessionLocal()
  users = db.query(User).all()
  db.close()
  return users


@app.post("/api/usuarios")
def create_user(user: UserCreate):
  db = SessionLocal()
  db_user = User(nombre=user.nombre)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  db.close()
  return db_user
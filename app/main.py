from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Initialize FastAPI
app = FastAPI()

'''
DATABASE
'''
#Database Connection Information
DATABASE_URL = "sqlite:///./todos.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Define Model
class Todo(Base):
    __tablename__="todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

#Initialize DataBase's Table
Base.metadata.create_all(bind=engine)

#資料驗證
'''
VALIDATION
'''
#Pydantic
class TodoBase(BaseModel):
    title: str
    description:str | None = None
    completed: bool = False

class TodoCreate(TodoBase):#繼承TodoBase class
    pass
class TodoResponse(TodoBase):
    id:int #會自動產生

    class Config:
        orm_mode = True

#Database Injection db注入
def get_db():
    db = SessionLocal() #使用SessionLocal與DB連線
    try:
        yield db
    finally:
        db.close() 

'''
ROUTING
'''
#Method->toList==>post->create , read->get , put->update , delete->delete
@app.post("/todos", response_model=TodoResponse)
def create_todos(todo: TodoCreate,db: Session = Depends(get_db())):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)#加入紀錄，但並沒有真正寫入資料庫
    db.commit()#加入資料庫
    db.refresh(db_todo)#更新資料庫
    return db_todo #使用者建立資料庫後會回傳建立的結果

@app.get("/todos", response_model=list[TodoResponse])#將每筆資料變成list形式
def read_todos(db: Session = Depends(get_db())):
    return db.query(Todo).all() #回傳資料庫所有資料

@app.get("/todo/{todo_id}",response_model=TodoResponse)#取出其中一筆
def read_todo(todo_id: int, db: Session = Depends(get_db())):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()#filter -> 篩選
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    return db_todo

@app.put("/todo/{todo_id}",response_model=TodoResponse)#更新一筆資料
def updata_todo(todo_id:int ,todo:TodoCreate, db: Session = Depends(get_db())):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todo/{todo_id}")#刪除資料
def delete_todo(todo_id: int, db: Session = Depends(get_db())):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail":"Todo deleted successfully"}
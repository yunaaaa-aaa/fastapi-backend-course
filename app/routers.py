from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import TodoCreate, TodoResponse
from .models import Todo
from .database import SessionLocal

router = APIRouter()


#Database Injection db注入
def get_db():
    db = SessionLocal() #使用SessionLocal與DB連線
    try:
        yield db
    finally:
        db.close() 

'''
ROUTING(路由)
'''
#Method->toList==>post->create , read->get , put->update , delete->delete
@router.post("/todos", response_model=TodoResponse)
def create_todos(todo: TodoCreate,db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)#加入紀錄，但並沒有真正寫入資料庫
    db.commit()#加入資料庫
    db.refresh(db_todo)#更新資料庫
    return db_todo #使用者建立資料庫後會回傳建立的結果

@router.get("/todos", response_model=list[TodoResponse])#將每筆資料變成list形式
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all() #回傳資料庫所有資料

@router.get("/todo/{todo_id}",response_model=TodoResponse)#取出其中一筆
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()#filter -> 篩選
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    return db_todo

@router.put("/todo/{todo_id}",response_model=TodoResponse)#更新一筆資料
def updata_todo(todo_id:int ,todo:TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todo/{todo_id}")#刪除資料
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail":"Todo deleted successfully"}
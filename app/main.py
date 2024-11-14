from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    description:str=None

@app.get("/") #定義路徑 get->方法
def read_root(): #當使用者在瀏覽器打開這個路徑，這個function就會回傳
    return {"Hello": "World"}
@app.get('/哈囉')
def read_hello():
    return '<p>Hello World</p>'

@app.post("/items")
def create_item(item:Item):
    print(f"Received item: {item}")
    return {"message":"Item received","item":item}
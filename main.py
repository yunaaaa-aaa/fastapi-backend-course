from fastapi import FastAPI

app = FastAPI()


@app.get("/") #定義路徑 get->方法
def read_root(): #當使用者在瀏覽器打開這個路徑，這個function就會回傳
    return {"Hello": "World"}
@app.get('/哈囉')
def read_hello():
    return '<p>Hello World</p>'

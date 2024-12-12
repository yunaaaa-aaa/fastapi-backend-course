from pydantic import BaseModel

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
       from_attributes = True


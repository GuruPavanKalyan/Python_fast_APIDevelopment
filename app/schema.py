from typing import Optional
from pydantic import BaseModel

class Post_sce(BaseModel):
    title:str
    content:str
    published:bool=True # this would be optional, if user doesnot given i/p it would be true.
    rating: Optional[int] = None
    id:int
from fastapi import Body, FastAPI, HTTPException, Response,status,Request,Depends
from pydantic import BaseModel
from app.schema import Post_sce
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.database import engine,SessionLocal
from app import models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware




models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins=['*']# here we can connect using different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#depedency for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    


#for post storage
my_list=[{
  "title": "pavan",
  "content": "kalyan",
  "published":True,
  "rating": 0,
  "id": 1
}]

while True:
    try:
       conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password='bguru',cursor_factory=RealDictCursor)
       cursor=conn.cursor()
       print("database connection success")
       break
    except Exception as error:
       print("database connection failed")  
       time.sleep()  
    finally:    
       pass
    
# def post_id(id):
#     for i in my_list:
#         if i['id']==int(id):
#             k = i.index()
#             return k
def find_post_id(id):
    for i,p in enumerate(my_list):
        if p['id']==id:
            return i


@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return {"status":posts}


#only takes the first url
@app.get("/ip")
async def get_ip(request: Request):
    client_host = request.client.host
    return {"ip": client_host}
@app.get("/")
async def root():
    return {"message":"Welcome to My API !!"}
@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    post= cursor.fetchall()
    print(post)
    return {"data":post}

@app.post("/post",status_code=status.HTTP_201_CREATED)
# async def createposts(payload:dict=Body(...)): #this helps to get the data without using schema
async def createposts(new_post:Post_sce):
    #updating through data base
    cursor.execute("INSERT INTO posts (title,content,published)VALUES (%s,%s,%s) RETURNING *",(new_post.title,new_post.content,new_post.published))
    post = cursor.fetchone()
    conn.commit()
    #print(payload)
    # print(new_post)
    # print(len(my_list))
    # new_post_dict =new_post.dict()
    # new_post_dict["id"] =len(my_list)+1
    # my_list.append(new_post_dict)
    # return {"new_post":f"title: {payload['title']} content:{payload['content']}"}
    return {"data":post}

#getting one post using id
@app.get("/post/{id}")
async def get_post_id(id:str,response:Response):
    cursor.execute("select * from posts where id=%s",(str(id),))
    post = cursor.fetchone()
    print(post)
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with {id}")
    return {"data":post}
    # if int(id) > len(my_list):
    #     response.status_code=status.HTTP_404_NOT_FOUND
    #     return {
    #         "error":"Post with this ID doesn't exit!"
            
    #     }
    
    # for post in my_list:
    #     if post["id"]==id:
    #         return{
    #             "data":post
    #         }
    #     else:
    #         response.status_code=status.HTTP_404_NOT_FOUND

#delete
@app.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str,response:Response):
    cursor.execute("delete from posts where id=%s returning *",(str(id),))
    new_post= cursor.fetchone()
    conn.commit()
    # index= find_post_id(id)
    if new_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found with {id}")
    # else:
    #     my_list.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updating a post
@app.put("/posts/{id}")
async def update_post(id:int,post:Post_sce):
    cursor.execute("update posts set title =%s,content=%s,published=%s where = %s,returning *",(post.title,post.content,post.published,str(id)))
    #update=cursor.fetchone()
    new_post=cursor.fetchone()
    conn.commit()
    print(new_post)
    # ind=find_post_id(id)
    # print(id)
    if new_post==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    # post_dict = post.dict()
    # post_dict['id']=id
    # print(my_list[ind])
    # print(post_dict)
    # print(post)
    # my_list[ind]=post_dict
    return({"updated":new_post})
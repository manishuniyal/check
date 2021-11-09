from typing import NewType, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from random import randrange
import psycopg
import time

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

app = FastAPI()
class Post_match(BaseModel):
    title: str
    post: str
    blog_live:bool=True
    rating :Optional[int]=None

while True:

    try:

        # Connect to an existing database
        conn=psycopg.connect("dbname=api user=manish host=localhost password=pooja1@A")          # Open a cursor to perform database operations
        cur= conn.cursor()
        print("okkk connection established ")
        break
    except Exception as error:
        print("Error",error)
        time.sleep(2)

mypost=[{"title":"this is the title of the post", "content":"this is the content of the post", "id":1}
,{"title":"this is the title of the post", "content":"this is the content of the post", "id":2}
]

@app.get("/")
def read_root():
    return [{"Hello": "Worlds"}]


@app.get("/items/{item_id}")
# or  http://127.0.0.1:8000/items/5?q=somequery
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "Optional string": q}

@app.get("/dr")
def more_post():
    return {"data":mypost}

@app.get("/dr/latest")
def latest_post():
    post=len(mypost)-1
    print(post)
    return {"t":mypost[post]}

def search_post(post_id):
    for i in mypost:
        if i["id"]== post_id:
            return i

@app.get("/dr/{id}")
##def more_post(id:int, response:Response):
def more_post(id:int):
    print(id)
    find_post=search_post(id)
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not find")
        ##response.status_code=status.HTTP_404_NOT_FOUND
        ##return {"message":f"post with id: {id} not find"}
    #return {"the post id is": mypost[int(id)]}
    return {"good": find_post}

def find_post_index(id):
    for index, p in enumerate(mypost):
        if p['id']==id:
            return index
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index= find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"the id: {id} does't exist")
    mypost.pop(index)
    #return {"message": f"post is successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id:int,post:Post_match):
    print(post)
    index= find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"the id: {id} does't exist")
    mypost_dict=post.dict()
    mypost_dict['id'] =id  
    mypost[index]=mypost_dict
    return{"data":mypost_dict} 


@app.post("/post_req1")
def post_data1(received_data_payload: dict=Body(...)):
    print(received_data_payload)
    return {" Latest Post":f" Title: {received_data_payload['title']} Post_Body {received_data_payload['content']}"}


@app.post("/post_req2")
def post_data2(new_post: Post_match):
    print(new_post.rating,"\n", new_post.blog_live)
    print(new_post.dict())
    return {"This is received title": new_post.title, "This is received post":new_post.post, "parent": new_post}



@app.post("/dr", status_code=HTTP_201_CREATED)
#def post_data2(new_post: Post_match):
def create_post(new_post: Post_match):

    post_dict=new_post.dict()
    post_dict["id"]=randrange(0,100000)
    mypost.append(post_dict)
     
    return {"data": post_dict}
    #return {"This is received title": new_post.title, "This is received post":new_post.post}



from typing import Dict, Optional, List
from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    # Optional：入力必須の解除
    published: Optional[bool]
    nb_comments: int
    # リスト型で取得する
    tags: List[str] = []
    # 辞書型で取得する
    metadata: Dict[str, str] = {"key": "val"}
    # 他のBaseModelを継承できる
    image: Optional[Image] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "data": blog,
        "id": id,
        "version": version
    }
    
@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
    blog: BlogModel, 
    id: int, 
    # Query: クエリパラメータにオプションをつける。
    comment_title: str = Query(
        None, 
        title ="title of the comment",
        description="Some description for comment_title",
        alias="commetTitle",
        deprecated=True,
    ),
    # Body: リクエストボディにオプションをつけられる
    content: str = Body(
        ..., # ...は入力必須
        min_length=3
    ),
    # vというクエリパラメータをリスト形式で受け取る
    v: Optional[List[str]] = Query(None),
    # Path: int型のパスパラメータにオプションをつける
    comment_id: int = Path(None, gt=0, le=10)
    ):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id,
        "comment_title": comment_title,
        "content": content,
        "version": v
    }
    
    
def required_functionality():
    return {'message': 'req message!'}
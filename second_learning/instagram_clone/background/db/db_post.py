from fastapi import HTTPException, status
from routers.schemas import PostBase
from db.models import DbPost
from sqlalchemy.orm.session import Session
from datetime import datetime


def create_post(db: Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.now(),
        user_id = request.creater_id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def get_all_post(db: Session):
    return db.query(DbPost).all()
    
    
def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='投稿が存在しません'
        )
    
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='投稿の削除権限がありません'
        )
        
    db.delete(post)
    db.commit()
    
    return 'ok'
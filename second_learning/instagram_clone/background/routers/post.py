import random
import shutil
import string
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from auth.oauth import get_current_user
from routers.schemas import PostBase, PostDisplay, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_post
from typing import List

router = APIRouter(
    prefix='/post',
    tags=['post']
)


image_url_types = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='画像タイプがうまく識別できません')

    return db_post.create_post(db, request)
    
    
@router.get('', response_model=List[PostDisplay])
def get_all_post(db: Session = Depends(get_db)):
    return db_post.get_all_post(db)
    
@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserDisplay = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for _ in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
        
    return {'filename': path}
    

@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)

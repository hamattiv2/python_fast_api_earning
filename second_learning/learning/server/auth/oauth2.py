from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = '68e6ca1391725356ce7b39fdfc7ef26b93f96d236a565f256564f99b84788e91'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
        
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='認証に失敗しました',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db_user.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    return user 
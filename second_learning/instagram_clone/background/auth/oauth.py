from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from db import db_user
from db.database import get_db


# トークン発行元のURLパスを定義(http://ドメイン/login)
oauth2_shceme = OAuth2PasswordBearer(tokenUrl='login')

# openssl rand -hex 32
SECRET_KEY = 'eb9527943262f38ebe234281ea49388e6d6e84c3abdd9747c38a3c2d4dc5e76d'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ログイン時のアクセストークンを生成する"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
        
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    


def get_current_user(token: str = Depends(oauth2_shceme), db: Session = Depends(get_db)):
    """アクセストークンをもとにユーザー情報を取得する"""
    credentilas_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='認証情報の取得に失敗しました',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    print(token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get('sub')

        if username is None:
            raise credentilas_exception
        
    except JWTError:
        raise credentilas_exception

    user = db_user.get_user_by_username(db, username=username)

    if user is None:
        raise credentilas_exception

    return user
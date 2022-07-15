from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash():
    def bcrypt(password: str):
        """パスワード暗号化"""
        return pwd_cxt.hash(password)
        
    def verify(hashed_password, plain_password):
        """パスワード検証"""
        return pwd_cxt.verify(plain_password, hashed_password)

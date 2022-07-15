from .database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    items = relationship('DbPost', back_populates='user')
    
    
class DbPost(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255))
    image_url_type = Column(String(255))
    caption = Column(Text)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
    comments = relationship('DbComment', back_populates='post')
    
class DbComment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    username = Column(String(255))
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('DbPost', back_populates='comments')
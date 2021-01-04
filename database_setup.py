#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, VARCHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()






class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(Integer, nullable=False, default=1)
    job_title = Column(String(50), default='')
    # the image should be uploaded first to the static folder there is default value if wrong file path 
    image_link = Column(String(500), default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNQwe1wCiZ6X_-yw_WCj_zxYeY3a4rSfQ_MA&usqp=CAU')
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name':self.start,
			'job_title':self.job_title,
			'image_link': self.image_link,
        }

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(), nullable=False)
    post_date = Column(String(255), nullable=False)
    image = Column(String(255), default='https://www.onlinetefltraining.com/wp-content/uploads/2013/08/2173808.jpg')
    section = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'post_date': self.post_date,
            'section': self.section,
            'user_id': self.user_id,
        }

class PostMeta(Base):
    __tablename__ = 'post_meta'
    id = Column(Integer, primary_key=True)
	# example key like  value 1
    meta_key = Column(String())
    meta_name = Column(String())
    meta_value = Column(String())
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'meta_key': self.meta_key,
            'meta_name': self.meta_name,
            'meta_value': self.meta_value,
            'post_id': self.post_id,
        }

engine = create_engine('sqlite:///the_database.db')
Base.metadata.create_all(engine)

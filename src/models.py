from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er


db = SQLAlchemy()


likes = Table ('likes', db.Model.metadata, 
            Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
            Column('post_id', Integer, ForeignKey('post.id'), primary_key=True)
            )

follower = Table ('follower', db.Model.metadata,
                  Column('user_from_id',Integer, ForeignKey('user.id'), primary_key=True),
                  Column('user_to_id',Integer, ForeignKey('user.id'), primary_key=True))

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(250), nullable= False)
    lastname: Mapped[str] = mapped_column(String(250), nullable= False)
    email: Mapped[str] = mapped_column(String(250), nullable = False)
    #Relaciones
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    liked_posts: Mapped[list['Post']] = relationship('Post',secondary = likes ,back_populates='linking_users')
    follower: Mapped[list['User']] = relationship('User',secondary = follower ,back_populates='follower')


    def serialize(self):
        return {"id":self.id, "username":self.username}



class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    caption: Mapped[str] = mapped_column(String(250), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    #Relaciones
    user: Mapped[list['User']] = relationship('User', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')
    liked_user: Mapped[list['User']] = relationship('User',secondary = likes ,back_populates='linking_users')




class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    text: Mapped[str] = mapped_column(String(250), nullable = False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    #Relaciones
    user: Mapped[list['User']] = relationship('User', back_populates='comments')
    post: Mapped[list['Post']] = relationship('Post', back_populates='comments')







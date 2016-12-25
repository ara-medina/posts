from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, DateTime, Text, Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime

from . import app


from posts import app

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    
    def as_dictionary(self):
        post = {
            "id": self.id,
            "title": self.title,
            "body": self.body
        }
        return post
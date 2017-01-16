from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class Post(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(Date)

    def to_json(self):
        """Returns a Json type object."""
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "creation_date": self.creation_date.strftime('%b %d, %Y'),
        }


Index('index', Post.title, unique=True, mysql_length=255)

from config.database import Base
from sqlalchemy import Column, Integer, String


# Movie is a SQLAlchemy model, because it inherits from Base
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    category = Column(String)

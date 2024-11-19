from sqlalchemy import Column, Date, Integer, String, Text
from database.connect import Base

class Author(Base):
    __tablename__ = "Authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=False)
    death_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.first_name} {self.last_name}, birth_date={self.birth_date}, death_date={self.death_date})>"

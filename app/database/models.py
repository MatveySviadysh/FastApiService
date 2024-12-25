from sqlalchemy import Column, Date, Integer, String, Text, CheckConstraint
from database.connect import Base

class Author(Base):
    __tablename__ = "Authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    patronymic = Column(String(100), nullable=True)
    photo = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=False)
    death_date = Column(Date, nullable=True)

    __table_args__ = (
        CheckConstraint('birth_date <= death_date', name='check_dates'),
    )

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.first_name} {self.last_name}, birth_date={self.birth_date})>"

    @property
    def full_name(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"

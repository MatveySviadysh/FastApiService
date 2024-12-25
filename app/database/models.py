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
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "photo": self.photo,
            "bio": self.bio,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "death_date": self.death_date.isoformat() if self.death_date else None,
            "full_name": self.full_name
        }
from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date

class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str] = mapped_column(Text, nullable=False)
    
    
class Post(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
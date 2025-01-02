from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CreateTable
from typing import Optional
from Module17.module_17_2.app.backend.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[Optional[str]]
    content: Mapped[Optional[str]]
    priority: Mapped[Optional[int]] = mapped_column(default=0)
    completed: Mapped[Optional[bool]] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    slug: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    user: Mapped['User'] = relationship(back_populates='tasks')


print(CreateTable(Task.__table__))

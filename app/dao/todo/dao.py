# import datetime
# from typing import Optional
#
# from sqlalchemy import String, Column, DateTime, Boolean, ForeignKey
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
#
# from app.base.main import get_engine
# from app.dao.user import dao
#
# engine = get_engine()
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# class Todo(Base):
#     __tablename__      = "Todo"
#
#     id              : Mapped[int]               = mapped_column(primary_key = True)
#     title           : Mapped[str]               = mapped_column(String(60))
#     desc            : Mapped[Optional[str] ]
#     created_at      : Mapped[datetime]          = Column(DateTime, default=datetime.datetime.utcnow)
#     is_completed    : Mapped[bool]              = Column(Boolean, default=False)
#
#     user_id         : Mapped[int]               = mapped_column(ForeignKey("User.id"))
#     user            : Mapped["dao.User"]       = relationship(back_populates="todo")
#
#
# Base.metadata.create_all(engine)
#

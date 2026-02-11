from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column



class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime,
    default = datetime.now,
    comment = "创建时间"
    )
    updated_at: Mapped[DateTime] = mapped_column(DateTime,
    default = datetime.now,
    onupdate = datetime.now,
    comment = "更新时间"
    )

class Category(Base):
    __tablename__ = "news_category"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,comment="分类ID")
    name : Mapped[str] = mapped_column(String(50), nullable=False,unique=True,comment="分类名称")
    sort_order : Mapped[int] = mapped_column(Integer, nullable=False,default=0,comment="排序顺序")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, sort_order={self.sort_order})"

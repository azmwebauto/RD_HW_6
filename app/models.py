from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class CveModel(Base):
    __tablename__ = 'cves'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    cve_id: Mapped[str] = mapped_column(nullable=False, unique=True)

    description: Mapped[str] = mapped_column(nullable=True, default='No description available')
    title: Mapped[str] = mapped_column(nullable=True, default='Unknown Title')
    problem_types: Mapped[str] = mapped_column(nullable=True, default='No problem types available')

    published_date: Mapped[datetime] = mapped_column(nullable=False)
    last_modified_date: Mapped[datetime] = mapped_column(nullable=False)

    raw_info: Mapped[dict] = mapped_column('raw_info', JSONB)

    def to_dict(self):
        return {
            'id': self.id,
            'cve_id': self.cve_id,
            'description': self.description,
            'title': self.title,
            'problem_types': self.problem_types,
            'published_date': self.published_date,
            'last_modified_date': self.last_modified_date,
            'raw_info': self.raw_info,
        }

from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid


Base = declarative_base()


class Image(Base):
    __tablename__ = "images"

    imageId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    userId = Column(String, nullable=False)
    url = Column(String, nullable=False)
    originalname = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    kelas = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    long_desc = Column(String, nullable=False)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=datetime.utcnow, nullable=False)


def upgrade(migrate_engine):
    Image.__table__.create(bind=migrate_engine)



def downgrade(migrate_engine):
    Base.metadata.bind = migrate_engine
    Image.__table__.drop()

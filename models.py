from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

# You will need to point this to wherever your declarative base is
from ...models import Base

class Notification(Base):
    __tablename__ = 'notifications'
    user          = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    posted        = Column(DateTime, nullable=False)
    expiration    = Column(DateTime)
    
    message       = Column(String, nullable=False)
    meta          = Column(String, nullable=False)

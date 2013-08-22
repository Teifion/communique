from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

# You will need to point this to wherever your declarative base is
from ..models import Base

class Notification(Base):
    __tablename__ = 'notifications'
    id            = Column(Integer, primary_key=True)
    user          = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    posted        = Column(DateTime, nullable=False)
    expires       = Column(DateTime)
    
    message       = Column(String, nullable=False)
    category      = Column(String, nullable=False)
    data          = Column(String, nullable=False)

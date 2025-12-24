from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Transaction(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    time = Column(TIMESTAMP)
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])


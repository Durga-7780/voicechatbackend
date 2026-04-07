from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organizations = relationship("Organization", secondary="user_organizations", back_populates="users")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    billing_plan_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", secondary="user_organizations", back_populates="organizations")
    api_keys = relationship("ApiKey", back_populates="organization")
    bot_configs = relationship("BotConfig", back_populates="organization")

class UserOrganization(Base):
    __tablename__ = "user_organizations"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    service = Column(String(50)) # openai, groq, deepgram, elevenlabs
    masked_key = Column(String(255))
    encrypted_key = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="api_keys")

class BotConfig(Base):
    __tablename__ = "bot_configs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(String(255))
    system_prompt = Column(Text)
    voice_id = Column(String(100), nullable=True)
    llm_model = Column(String(100), default="gpt-3.5-turbo")
    temperature = Column(Float, default=0.7)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="bot_configs")

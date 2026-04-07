from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# --- Pydantic Schemas ---
class BotConfigBase(BaseModel):
    name: str
    system_prompt: str
    voice_id: Optional[str] = None
    llm_model: str = "gpt-3.5-turbo"
    temperature: float = 0.7

class BotConfig(BotConfigBase):
    id: int
    organization_id: int
    class Config:
        from_attributes = True

class ApiKeyBase(BaseModel):
    service: str
    key: str

class ApiKeyResponse(BaseModel):
    id: int
    service: str
    masked_key: str
    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/bot-configs", response_model=List[BotConfig])
def read_bot_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    configs = db.query(models.BotConfig).offset(skip).limit(limit).all()
    return configs

@router.post("/bot-configs", response_model=BotConfig)
def create_bot_config(config: BotConfigBase, db: Session = Depends(get_db)):
    # For now, assigning to a mock organization ID = 1
    db_config = models.BotConfig(**config.dict(), organization_id=1)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/api-keys", response_model=List[ApiKeyResponse])
def read_api_keys(db: Session = Depends(get_db)):
    return db.query(models.ApiKey).all()

@router.post("/api-keys", response_model=ApiKeyResponse)
def create_api_key(api_key: ApiKeyBase, db: Session = Depends(get_db)):
    masked = api_key.key[:4] + "*" * (len(api_key.key) - 8) + api_key.key[-4:]
    db_key = models.ApiKey(
        service=api_key.service,
        masked_key=masked,
        encrypted_key="encoded_" + api_key.key, # Mock encryption
        organization_id=1
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

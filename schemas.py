from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "ANALYST"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class SessionResponse(BaseModel):
    id: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    last_activity: datetime.datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_active: bool
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    account_id: str
    event_type: str
    ip_address: str
    location: Optional[str] = None
    resource: Optional[str] = None
    api_name: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    timestamp: datetime.datetime
    risk_contribution: int
    is_anomalous: bool
    detection_reason: Optional[str] = None
    class Config:
        from_attributes = True

class CloudAccountBase(BaseModel):
    account_name: str
    user_id: int

class CloudAccountResponse(CloudAccountBase):
    id: str
    risk_score: int
    severity: str
    status: str
    last_login: Optional[datetime.datetime] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    incident_count: int
    class Config:
        from_attributes = True

class IncidentBase(BaseModel):
    account_id: str
    risk_score: int
    severity: str
    status: str
    main_reason: str

class IncidentResponse(IncidentBase):
    id: str
    created_at: datetime.datetime
    ml_analysis: Optional[Any] = None
    stat_analysis: Optional[Any] = None
    graph_analysis: Optional[Any] = None
    class Config:
        from_attributes = True

class SimulateRequest(BaseModel):
    scenario: str = "account_takeover"

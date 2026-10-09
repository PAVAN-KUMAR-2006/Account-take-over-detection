from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="ANALYST")
    is_active = Column(Boolean, default=True)
    failed_login_count = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    revoked_at = Column(DateTime, nullable=True)

class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    email_or_username = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    success = Column(Boolean)
    failure_reason = Column(String, nullable=True)

class CloudAccount(Base):
    __tablename__ = "cloud_accounts"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_name = Column(String)
    risk_score = Column(Integer, default=0)
    severity = Column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="ACTIVE") # ACTIVE, CONTAINED, SUSPENDED
    last_login = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    location = Column(String, nullable=True)
    incident_count = Column(Integer, default=0)
    
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("cloud_accounts.id"))
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String)
    location = Column(String, nullable=True)
    resource = Column(String, nullable=True)
    api_name = Column(String, nullable=True)
    risk_contribution = Column(Integer, default=0)
    is_anomalous = Column(Boolean, default=False)
    detection_reason = Column(String, nullable=True)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("cloud_accounts.id"))
    risk_score = Column(Integer)
    severity = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="OPEN") # OPEN, INVESTIGATING, CONTAINED, RESOLVED, FALSE_POSITIVE
    main_reason = Column(String)
    ml_analysis = Column(JSON, nullable=True)
    stat_analysis = Column(JSON, nullable=True)
    graph_analysis = Column(JSON, nullable=True)

class ResponseAction(Base):
    __tablename__ = "response_actions"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    performed_by = Column(Integer, ForeignKey("users.id"))

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    target = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String, nullable=True)
    metadata_json = Column(String, nullable=True)

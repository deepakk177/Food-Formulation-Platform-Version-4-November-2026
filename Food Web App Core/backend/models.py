import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator, CHAR
import datetime

from database import Base
from sqlalchemy.orm import relationship

# Custom UUID type descriptor that works on both SQLite and PostgreSQL
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(32), storing as string.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return value.hex
            else:
                return uuid.UUID(value).hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value

class User(Base):
    __tablename__ = "users"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="Guided User") # Guided User, Expert User, Administrator
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    query = Column(String, nullable=True)
    status = Column(String, default="Pending") # Pending, Formulated, Validated
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    formulations = relationship("Formulation", back_populates="project", cascade="all, delete-orphan")

class Formulation(Base):
    __tablename__ = "formulations"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID(), ForeignKey("projects.id"))
    version = Column(String, default="V1.0")
    composition = Column(JSON, nullable=False) # Ingredients list + percentages
    functional_coverage = Column(JSON, nullable=False) # Coverage list & completeness score
    performance_prediction = Column(JSON, nullable=False) # Viscosity, calories, texture, shelf life
    process_recommendations = Column(JSON, nullable=False) # Processing steps
    status = Column(String, default="Draft")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="formulations")
    compliance_logs = relationship("ComplianceLog", back_populates="formulation", cascade="all, delete-orphan")

class ComplianceLog(Base):
    __tablename__ = "compliance_logs"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    formulation_id = Column(GUID(), ForeignKey("formulations.id"))
    region = Column(String, nullable=False) # FSSAI, FDA, EFSA
    status = Column(String, nullable=False) # Passed, Warning, Failed
    alerts = Column(JSON, nullable=False) # List of alert strings
    verified_at = Column(DateTime, default=datetime.datetime.utcnow)

    formulation = relationship("Formulation", back_populates="compliance_logs")

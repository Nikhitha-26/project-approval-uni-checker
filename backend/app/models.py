import uuid
from sqlalchemy import Column, String, Enum, Integer, DateTime, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY as PG_ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
import enum

# pgvector support
from sqlalchemy.dialects.postgresql import VECTOR

Base = declarative_base()

class ProjectStatus(enum.Enum):
    PRECHECK = "PRECHECK"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"

class UserRole(enum.Enum):
    STUDENT = "STUDENT"
    TEACHER_APPROVER = "TEACHER_APPROVER"
    EXAMINER = "EXAMINER"

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_name = Column(String, nullable=False)
    student_roll = Column(String, nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    tags = Column(PG_ARRAY(String), nullable=True)
    department = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    embedding = Column(VECTOR(384), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PRECHECK, nullable=False)
    final_report_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

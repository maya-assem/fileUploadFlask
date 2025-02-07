from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os

Base = declarative_base()

class CallRecord(Base):
    __tablename__ = 'call_records'

    id = Column(Integer, primary_key=True)
    call_id = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, nullable=True)
    call_from = Column(String, nullable=True)
    call_to = Column(String, nullable=True)
    duration = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    recording_file = Column(String, nullable=True)
    call_date = Column(Date, nullable=True)
    is_fresh_lead = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    ring_duration = Column(Float, nullable=True)
    talk_duration = Column(Float, nullable=True)
    communication_type = Column(String, nullable=True)

class ChatRecord(Base):
    __tablename__ = 'chat_records'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    client = Column(String, nullable=True)
    messages = Column(Integer, nullable=True)
    employee = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=True)
    closed_on = Column(DateTime, nullable=True)
    response_time = Column(Float, nullable=True)
    lead_date = Column(Date, nullable=True)
    phone_number = Column(String, nullable=True)
    is_fresh_lead = Column(Boolean, default=False)
    crm_record = Column(Boolean, default=False)
    conversation_duration = Column(Integer, nullable=True)
    initial_response_time = Column(Integer, nullable=True)
    average_response_time = Column(Integer, nullable=True)

def init_db():
    # Fixed connection string for SQL Server using Windows Authentication
    connection_string = (
        "mssql+pyodbc://DESKTOP-R753PEO/DataUploaderDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    return engine
from datetime import datetime
import uuid
from sqlalchemy import ARRAY, JSON, Column, DateTime, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db.config import engine

Base = declarative_base()
def create_tables():
    Base.metadata.create_all(engine)


class EmailMessage(Base):
    __tablename__ = 'email_messages'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False, default='')
    sender = Column(String, nullable=False)
    to_emails = Column(String, nullable=False, default='')
    label_ids = Column(ARRAY(String), nullable=False, default=[])
    email_type = Column(Enum('sent', 'received', name='email_types'), nullable=False)
    raw_data = Column(JSON, nullable=False)
    status = Column(Enum('unprocessed', 'processed', name='email_status_types'), nullable=False, default='unprocessed')
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"<EmailMessage(id='{self.id}', message_id='{self.message_id}', subject='{self.subject}', sender='{self.sender}', recipient='{self.recipients}', status='{self.status}')>"
import os
from sqlalchemy.orm import sessionmaker
from .models import CallRecord, ChatRecord
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from contextlib import contextmanager
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

class DatabaseOperations:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def store_call_records(self, df):
        """Store call records with upsert operation to handle duplicates"""
        with self.session_scope() as session:
            for _, row in df.iterrows():
                stmt = insert(CallRecord).values(
                    call_id=row['ID'],
                    timestamp=pd.to_datetime(row['Time']),
                    call_from=row['Call From'],
                    call_to=row['Call To'],
                    duration=float(row['Call Duration']) if pd.notna(row['Call Duration']) else 0.0,
                    status=row['Status'],
                    recording_file=str(row['Recording File']) if pd.notna(row['Recording File']) else None,
                    call_date=pd.to_datetime(row['Time']).date(),
                    is_fresh_lead=row.get('is_fresh_lead', False),
                    source=row.get('source')
                )

                # Add ON CONFLICT clause for upsert
                stmt = stmt.on_conflict_do_nothing(index_elements=['call_id'])
                session.execute(stmt)
            session.commit()

    def store_chat_records(self, df):
        """Store chat records with upsert operation to handle duplicates"""
        with self.session_scope() as session:
            for _, row in df.iterrows():
                stmt = insert(ChatRecord).values(
                    chat_id=str(row['#']),
                    type=row['Type'],
                    status=row['Status'],
                    channel=row['Channel'],
                    client=row['Client'],
                    messages=int(row['Messages']) if pd.notna(row['Messages']) else 0,
                    employee=row['Employee'],
                    created_on=pd.to_datetime(row['Created on']),
                    closed_on=pd.to_datetime(row['Agent closed on']) if pd.notna(row['Agent closed on']) else None,
                    response_time=float(row['Total response time']) if pd.notna(row['Total response time']) else 0.0,
                    lead_date=pd.to_datetime(row['Created on']).date(),
                    phone_number=str(row['Client']),
                    is_fresh_lead=row.get('is_fresh_lead', False)
                )

                # Add ON CONFLICT clause for upsert
                stmt = stmt.on_conflict_do_nothing(index_elements=['chat_id'])
                session.execute(stmt)
            session.commit()

    def get_database_connection_info(self):
        """Get database connection information for external tools"""
        return {
            'host': os.getenv('PGHOST'),
            'port': os.getenv('PGPORT'),
            'database': os.getenv('PGDATABASE'),
            'user': os.getenv('PGUSER')
        }
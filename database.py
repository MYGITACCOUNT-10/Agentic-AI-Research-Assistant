from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://user:password@localhost/research_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ResearchReport(Base):
    __tablename__ = "research_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    intent = Column(String)
    sub_questions = Column(JSON)
    synthesis = Column(JSON)
    final_report = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Ensure tables exist (in production use Alembic migrations)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to PostgreSQL. Assuming dev environment. Error: {e}")

def save_report_to_db(query, intent, sub_questions, synthesis, report_text):
    session = SessionLocal()
    try:
        new_report = ResearchReport(
            query=query,
            intent=intent,
            sub_questions=sub_questions,
            synthesis=synthesis,
            final_report=report_text
        )
        session.add(new_report)
        session.commit()
        session.refresh(new_report)
        return new_report.id
    except Exception as e:
        print(f"Database error (skipping save): {e}")
    finally:
        session.close()

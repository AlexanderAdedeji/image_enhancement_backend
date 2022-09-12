from app.database.sessions.session2 import SessionLocal

def get_db2():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
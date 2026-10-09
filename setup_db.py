import os
from database import SessionLocal, engine
import models
import auth

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(models.User).filter(models.User.email == "test.admin@company.com").first()
    if not admin:
        hashed_password = auth.get_password_hash("Admin123!")
        admin = models.User(
            name="System Admin",
            email="test.admin@company.com",
            password_hash=hashed_password,
            role="ADMIN"
        )
        db.add(admin)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin already exists.")
        
    db.close()

if __name__ == "__main__":
    init_db()

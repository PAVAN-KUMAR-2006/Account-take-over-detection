from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth, accounts, incidents, simulation, logs

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI26CY01 - Cloud Account Takeover Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
app.include_router(simulation.router, prefix="/api/demo", tags=["demo"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])

@app.get("/")
def read_root():
    return {"message": "Cloud Security API is running"}

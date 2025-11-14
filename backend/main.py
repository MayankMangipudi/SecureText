from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import database
from app.database import Base, engine

# IMPORTANT: Import all models BEFORE creating tables
from app.models.user import User
from app.models.history import History

# Now create all tables
Base.metadata.create_all(bind=engine)

# Import routes after database setup
from app.routes import auth_routes, crypto_routes, history_routes, learn_routes

app = FastAPI(title="SecureText API", docs_url="/docs", redoc_url="/redoc")

# CORS - Add your custom domain
allowed_origins = [
    "http://localhost:8080",
    "https://secure-text-vit.vercel.app",
    "https://secure-text-vit-*.vercel.app",
    "https://securetext.mayankmangipudi.me",  # ✅ Add custom domain
    "*"  # Remove this after testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes - DON'T add prefix here, routes already have it
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(crypto_routes.router, tags=["crypto"])
app.include_router(history_routes.router, tags=["history"])
app.include_router(learn_routes.router, tags=["learn"])

@app.get("/")
def root():
    return {
        "message": "SecureText API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# Debug: Print registered routes on startup
@app.on_event("startup")
async def startup_event():
    print("\n=== Registered Routes ===")
    for route in app.routes:
        if hasattr(route, "methods"):
            print(f"{route.methods} {route.path}")
    print("========================\n")
    
    # Debug: Check if tables exist
    print("\n=== Database Tables ===")
    print(f"Tables: {Base.metadata.tables.keys()}")
    print("=======================\n")

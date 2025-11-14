from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Now import with relative paths
from app.database import Base, engine
from app.routes import auth_routes, crypto_routes, history_routes, learn_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureText API", docs_url="/docs", redoc_url="/redoc")

# CORS - Allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes - Register routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(crypto_routes.router, prefix="/crypto", tags=["crypto"])
app.include_router(history_routes.router, prefix="/history", tags=["history"])
app.include_router(learn_routes.router, prefix="/learn", tags=["learn"])

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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import Base, engine
from backend.app.routes import auth_routes, crypto_routes, history_routes, learn_routes
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureText API", docs_url="/docs", redoc_url="/redoc")

# CORS - Allow Vercel frontend
allowed_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://secure-text-vit.vercel.app",  # ← Your actual Vercel URL
    "https://secure-text-vit-*.vercel.app",  # Preview deployments
    "https://securetext.mayankmangipudi.me",  # Your custom domain (when added)
    "*"  # Allow all temporarily for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
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

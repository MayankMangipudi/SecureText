from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.database import Base, engine
from backend.app.routes import auth_routes, crypto_routes, history_routes, learn_routes
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureText API")

# CORS - Allow your custom domain and Replit URLs
allowed_origins = [
    "*",  # For development
    "https://securetext.mayankmangipudi.me",  # Your custom domain
    "https://securetext.replit.app",  # Replit subdomain
    "https://*.replit.dev",  # Replit dev URLs
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(crypto_routes.router, tags=["crypto"])
app.include_router(history_routes.router, tags=["history"])
app.include_router(learn_routes.router, tags=["learn"])

# Serve static frontend files
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/health")
def health():
    return {"status": "healthy", "message": "SecureText API is running"}

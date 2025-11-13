from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import Base, engine
from backend.app.routes import auth_routes, crypto_routes, history_routes, learn_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureText API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, tags=["auth"])
app.include_router(crypto_routes.router, tags=["crypto"])
app.include_router(history_routes.router, tags=["history"])
app.include_router(learn_routes.router, tags=["learn"])

@app.get("/")
def root():
    return {"message": "SecureText API is running"}

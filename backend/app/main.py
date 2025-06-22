from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, admin

app = FastAPI(
    title="University Project Similarity Checker",
    description="SaaS backend for project similarity and approval workflow",
    version="1.0.0"
)

# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Health check route
@app.get("/health")
def health():
    return {"status": "ok"}
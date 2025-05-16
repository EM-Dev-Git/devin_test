from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.items import router as items_router

app = FastAPI(title="EM_test_project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(items_router)

@app.get("/")
async def root():
    return {"message": "Welcome to EM_test_project API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

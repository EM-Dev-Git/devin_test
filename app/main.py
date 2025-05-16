from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import os
from datetime import datetime

from app.database import engine, Base
from app.routes.items import router as items_router
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

log_filename = f"logs/app_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app_logger = logger

app = FastAPI(title="EM_test_project")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    method = request.method
    path = request.url.path
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    app_logger.info(f"{method} {path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app_logger.info("Application startup: CORS middleware configured")

app.include_router(auth_router)
app_logger.info("Application startup: Auth router registered")

app.include_router(items_router)
app_logger.info("Application startup: Item router registered")

@app.get("/")
async def root():
    app_logger.info("Root endpoint accessed")
    return {"message": "Welcome to EM_test_project API"}

@app.get("/health")
async def health_check():
    app_logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

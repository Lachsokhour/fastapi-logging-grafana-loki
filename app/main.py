from fastapi import FastAPI, Request, Response
import logging
import logging.config
import yaml
import time
import os

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Load logging config
with open("logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = Response("Internal server error", status_code=500)
    try:
        response = await call_next(request)
    finally:
        duration = time.time() - start_time
        logger.info({
            "method": request.method,
            "url": request.url.path,
            "status_code": response.status_code,
            "duration": round(duration, 4),
            "client": request.client.host
        })
    return response

@app.get("/")
async def root():
    logger.info("Hello from root endpoint")
    return {"message": "Hello World"}

@app.get("/error")
async def error():
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Error occurred: {str(e)}")
        return {"error": "Something went wrong"}

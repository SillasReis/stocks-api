import structlog
import uvicorn


logger = structlog.get_logger("api")


if __name__ == "__main__":
    logger.info("API starting")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

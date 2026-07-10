from fastapi import FastAPI

from app.api.routes import router

from app.core.logger import logger

app = FastAPI(
    title="Production RAG Chatbot",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():

    return {
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.on_event("startup")
def startup():

    logger.info("=" * 60)
    logger.info("Starting Production RAG Chatbot")
    logger.info("=" * 60)
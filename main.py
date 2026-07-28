from routes.chat_routes import router as chat_router
from routes.summary_routes import router as summary_router
from routes.compare_routes import router as compare_router
from routes.analytics_routes import router as analytics_router

from src.database.database import engine
from src.database.models import Base
from fastapi import FastAPI
from routes.document_routes import router

app = FastAPI(
    title="AI Research & Knowledge Assistant",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(chat_router)
app.include_router(summary_router)
app.include_router(compare_router)
app.include_router(analytics_router)

@app.get("/")
def home():
    return {
        "message": "AI Research & Knowledge Assistant API is running!"
    }
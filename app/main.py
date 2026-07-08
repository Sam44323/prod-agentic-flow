from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Sam44323 Prod-AI Agent", version="1.0.0")

# adding the router to the app for the API
app.include_router(router)

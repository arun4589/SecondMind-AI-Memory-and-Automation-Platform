from fastapi import FastAPI
from backend.services.secondmind_services import secondmind
from contextlib import asynccontextmanager
from backend.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting SecondMind...")

    await secondmind.initialize()

    yield

    print("Shutting down SecondMind...")

    await secondmind.cleanup()


app = FastAPI(
    title="SecondMind API",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.get("/")
async def root():
    return {
        "message": "SecondMind Running"
    }
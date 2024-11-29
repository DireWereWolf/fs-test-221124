import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.provision.entrypoints.fastapi_app import router as user_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(root_path="/api/v1")

origins = [
    "http://localhost:9000",
    "http://0.0.0.0:9000",
    "http://127.0.0.1:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="", tags=["Users"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch all exceptions inheriting from the base Exception class and return a 500 response.
    """
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal server error occurred.",
            "details": str(exc),
        },
    )

@app.get("/", status_code=200)
async def root():
    return


if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.getenv("HOST", "127.0.0.1")  # Default to 127.0.0.1 if not set
    port = int(os.getenv("PORT", 9001))    # Default to 9001 if not set

    # Run the server
    uvicorn.run(app, host=host, port=port)
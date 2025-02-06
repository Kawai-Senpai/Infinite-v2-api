from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from database.mongo import pingtest as mongo_pingtest
from datetime import datetime, timezone
from errors.error_logger import log_exception_with_request
import uvicorn
from routers.auth_route import clerk_auth

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"message": "Hello, Clerk!"}

@app.get("/protected")
@clerk_auth()
async def protected_route(user=None, request: Request = None):  # Add default value to user
    user_id = user.get("sub")
    return {"message": f"Hello, {user_id}"}

@app.get("/status")
async def status(request: Request):
    try:
        mongo_status = "up" if mongo_pingtest() else "down"
        return {
            "message": "Service status retrieved successfully.",
            "server": "API",
            "time": datetime.now(timezone.utc).isoformat() + "Z",
            "mongodb": mongo_status
        }
    except Exception as e:
        log_exception_with_request(e, status, request)
        return {
            "message": "Service status retrieval encountered an error.",
            "server": "API",
            "time": datetime.now(timezone.utc).isoformat() + "Z",
            "mongodb": "down",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=9000, reload=True)
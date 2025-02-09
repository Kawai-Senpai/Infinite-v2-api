from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.mongo import pingtest as mongo_pingtest
from datetime import datetime, timezone
from errors.error_logger import log_exception_with_request
import uvicorn
from routers import agent_route, chat_route, session_route
from dependencies.auth import get_current_user  # Add this import
from keys.keys import environment

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Change from '/agent' to '/agents' to match the other server's expectation
app.include_router(agent_route.router, prefix="/agents", tags=["agent"])
app.include_router(chat_route.router, prefix="/chat", tags=["chat"])
app.include_router(session_route.router, prefix="/sessions", tags=["session"])

@app.get("/protected")
async def protected_route(
    user: dict = Depends(get_current_user)  # Use the new dependency
):
    user_id = user.get("sub")
    return {"message": f"Hello, {user_id}"}

@app.get("/status")
@app.get("/")
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

if __name__ == "__main__" and environment == "development":
    uvicorn.run("_server:app", host="localhost", port=9000, reload=True)
from fastapi import APIRouter, HTTPException, Request, Body, Depends
from fastapi.responses import StreamingResponse
import httpx
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request
from utilities.error_handler import handle_request_error
from bson import ObjectId
from database.mongo import client as mongo_client

router = APIRouter()

@router.post("/agent/{session_id}")
async def chat(
    request: Request,
    session_id: str,
    agent_id: str,
    body: dict = Body(...),
    stream: bool = False,
    use_rag: bool = True,
    include_rich_response: bool = True,
    user: dict = Depends(get_current_user)
):
    try:
        db = mongo_client.ai
        session_doc = db.sessions.find_one({"_id": ObjectId(session_id)})
        if not session_doc:
            raise HTTPException(status_code=404, detail="Session not found")
        if session_doc.get("session_type") == "team":
            raise HTTPException(
                status_code=400,
                detail="Cannot use /agent endpoint for team sessions"
            )
        user_id = user.get("sub")
        url = f"{aiml_service_url}/chat/agent/{session_id}"
        params = {
            'agent_id': agent_id,
            'stream': stream,
            'use_rag': use_rag,
            'include_rich_response': include_rich_response
        }
        if stream:
            async def stream_bytes():
                async with httpx.AsyncClient(timeout=None) as client:  # Disable timeouts
                    async with client.stream('POST', url, params={**params, "user_id": user_id}, json=body) as response:
                        async for chunk in response.aiter_bytes():
                            yield chunk
            return StreamingResponse(
                stream_bytes(),
                media_type='text/event-stream',
                headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
            )
        else:
            return await forward_request('post', url, user_id=user_id, params=params, json=body)
    except Exception as e:
        await handle_request_error(e, chat, request)

@router.post("/team/{session_id}")
async def team_chat(
    request: Request,
    session_id: str,
    body: dict = Body(...),
    stream: bool = False,
    use_rag: bool = True,
    include_rich_response: bool = True,
    user: dict = Depends(get_current_user)
):
    try:
        db = mongo_client.ai
        session_doc = db.sessions.find_one({"_id": ObjectId(session_id)})
        if not session_doc:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Debug: log the trimmed session_type value
        session_type = session_doc.get("session_type", "").strip().lower()
        
        if not session_type.startswith("team"):
            raise HTTPException(status_code=400, detail="Not a team session")

        user_id = user.get("sub")
        url = f"{aiml_service_url}/chat/team/{session_id}"
        
        # Prepare request body
        request_body = {
            "message": body.get("message", ""),
            "user_id": user_id
        }
        
        params = {
            'stream': stream,
            'use_rag': use_rag,
            'include_rich_response': include_rich_response
        }
        
        if stream:
            async def stream_bytes():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream('POST', url, params=params, json=request_body) as response:
                        async for chunk in response.aiter_bytes():
                            yield chunk
            return StreamingResponse(
                stream_bytes(),
                media_type='text/event-stream',
                headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
            )
        else:
            response = await forward_request('post', url, params=params, json=request_body)
            if isinstance(response, dict) and "data" in response:
                return response["data"]
            return response
            
    except Exception as e:
        await handle_request_error(e, team_chat, request)

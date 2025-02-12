from fastapi import APIRouter, HTTPException, Request, Body, Depends
from fastapi.responses import StreamingResponse
import httpx
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request

router = APIRouter()

@router.post("/agent/{session_id}")
async def chat(
    request: Request,
    session_id: str,
    agent_id: str,
    body: dict = Body(...),
    stream: bool = False,
    use_rag: bool = True,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    url = f"{aiml_service_url}/chat/agent/{session_id}"
    params = {
        'agent_id': agent_id,
        'stream': stream,
        'use_rag': use_rag
    }
    
    if stream:
        async def stream_bytes():
            async with httpx.AsyncClient(timeout=None) as client:  # Disable timeouts
                async with client.stream('POST', url, params={**params, "user_id": user_id}, json=body) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
        return StreamingResponse(
            stream_bytes(),
            media_type='text/event-stream'
        )
    else:
        return await forward_request('post', url, user_id=user_id, params=params, json=body)

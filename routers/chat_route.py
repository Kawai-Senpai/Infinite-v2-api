from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import StreamingResponse
import httpx
from keys.keys import aiml_service_url
from .auth_route import clerk_auth

router = APIRouter()

@router.post("/agent/{session_id}")
@clerk_auth()
async def chat(
    user=None,
    request: Request = None,
    session_id: str = None,
    agent_id: str = None,
    body: dict = Body(...),
    stream: bool = False,
    use_rag: bool = True
):
    try:
        user_id = user.get("sub")
        url = f"{aiml_service_url}/chat/agent/{session_id}"
        params = {
            'agent_id': agent_id,
            'stream': stream,
            'use_rag': use_rag,
            'user_id': user_id
        }
        
        if stream:
            async with httpx.AsyncClient() as client:
                async with client.stream('POST', url, params=params, json=body) as response:
                    return StreamingResponse(
                        response.aiter_bytes(),
                        media_type='text/event-stream'
                    )
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params, json=body)
                return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

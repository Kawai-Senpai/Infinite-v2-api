from fastapi import APIRouter, HTTPException, Request, Body
import httpx
from keys.keys import aiml_service_url
from .auth_route import clerk_auth

router = APIRouter()

async def forward_request(method: str, path: str, user_id: str = None, **kwargs):
    url = f"{aiml_service_url}/session{path}"
    if user_id:
        kwargs['params'] = kwargs.get('params', {})
        kwargs['params']['user_id'] = user_id
    
    async with httpx.AsyncClient() as client:
        response = await getattr(client, method)(url, **kwargs)
        return response.json()

@router.post("/create")
@clerk_auth()
async def create_session(
    user=None, 
    request: Request = None,
    agent_id: str = None,
    max_context_results: int = 1
):
    try:
        user_id = user.get("sub")
        response = await forward_request('post', '/create',
            user_id=user_id,
            params={'agent_id': agent_id, 'max_context_results': max_context_results}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{session_id}")
@clerk_auth()
async def delete_session(user=None, request: Request = None, session_id: str = None):
    try:
        user_id = user.get("sub")
        response = await forward_request('delete', f'/delete/{session_id}',
            user_id=user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
@clerk_auth()
async def get_history(user=None, request: Request = None, session_id: str = None, limit: int = 20, skip: int = 0):
    try:
        user_id = user.get("sub")
        response = await forward_request('get', f'/history/{session_id}',
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/update/{session_id}")
@clerk_auth()
async def update_history(user=None, request: Request = None, session_id: str = None, role: str = None, content: str = None):
    try:
        user_id = user.get("sub")
        response = await forward_request('post', f'/history/update/{session_id}',
            user_id=user_id,
            json={'role': role, 'content': content}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/recent/{session_id}")
@clerk_auth()
async def get_recent_history(user=None, request: Request = None, session_id: str = None, limit: int = 20, skip: int = 0):
    try:
        user_id = user.get("sub")
        response = await forward_request('get', f'/history/recent/{session_id}',
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all/{user_id}")
@clerk_auth()
async def list_user_sessions(
    user=None, 
    request: Request = None, 
    user_id: str = None,
    limit: int = 20, 
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1
):
    try:
        response = await forward_request('get', f'/get_all/{user_id}',
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_by_agent/{agent_id}")
@clerk_auth()
async def list_agent_sessions(
    user=None,
    request: Request = None,
    agent_id: str = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1
):
    try:
        user_id = user.get("sub")
        response = await forward_request('get', f'/get_by_agent/{agent_id}',
            user_id=user_id,
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{session_id}")
@clerk_auth()
async def get_session_details(user=None, request: Request = None, session_id: str = None):
    try:
        user_id = user.get("sub")
        response = await forward_request('get', f'/get/{session_id}',
            user_id=user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

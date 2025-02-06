from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import JSONResponse
import httpx
from keys.keys import aiml_service_url
from .auth_route import clerk_auth

router = APIRouter()

async def forward_request(method: str, path: str, user_id: str = None, **kwargs):
    url = f"{aiml_service_url}/agent{path}"
    if user_id:
        kwargs['user_id'] = user_id
    
    try:
        async with httpx.AsyncClient() as client:
            response = await getattr(client, method)(url, **kwargs)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            return response.json()
    except httpx.HTTPStatusError as e:
        # Forward the same status code and error message from the AIML service
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except httpx.RequestError as e:
        # Network/connection errors
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/create")
@clerk_auth()
async def create_agent(user=None, request: Request = None, body: dict = Body(...)):
    try:
        user_id = user.get("sub")
        response = await forward_request('post', '/create', 
            user_id=user_id,
            json=body
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_public")
@clerk_auth()
async def get_public_agents(user=None, request: Request = None, limit: int = 20, skip: int = 0):
    try:
        response = await forward_request('get', '/get_public', 
            params={'limit': limit, 'skip': skip}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{agent_id}")
@clerk_auth()
async def delete_agent(user=None, request: Request = None, agent_id: str = None):
    try:
        user_id = user.get("sub")
        response = await forward_request('delete', f'/delete/{agent_id}',
            user_id=user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_approved")
@clerk_auth()
async def get_approved_agents(user=None, request: Request = None, limit: int = 20, skip: int = 0):
    try:
        response = await forward_request('get', '/get_approved',
            params={'limit': limit, 'skip': skip}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_system")
@clerk_auth()
async def get_system_agents(user=None, request: Request = None, limit: int = 20, skip: int = 0):
    try:
        response = await forward_request('get', '/get_system',
            params={'limit': limit, 'skip': skip}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_user/{user_id}")
@clerk_auth()
async def get_user_agents(
    user_id: str,
    request: Request,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1
):
    try:
        response = await forward_request('get', f'/get_user/{user_id}',
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{agent_id}")
@clerk_auth()
async def get_agent_details(agent_id: str, request: Request, user=None):
    try:
        response = await forward_request('get', f'/get/{agent_id}',
            user_id=user.get('sub')
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools")
@clerk_auth()
async def get_available_tools(user=None, request: Request = None):
    try:
        response = await forward_request('get', '/tools')
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

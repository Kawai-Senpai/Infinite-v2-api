from fastapi import APIRouter, HTTPException, Request, Body, Depends
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request

router = APIRouter()

@router.post("/create")
async def create_session(
    request: Request,
    agent_id: str,
    max_context_results: int = 1,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'post',
        f"{aiml_service_url}/sessions/create",
        user_id=user_id,
        params={'agent_id': agent_id, 'max_context_results': max_context_results}
    )

@router.delete("/delete/{session_id}")
async def delete_session(
    request: Request,
    session_id: str,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'delete',
        f"{aiml_service_url}/sessions/delete/{session_id}",
        user_id=user_id
    )

@router.get("/history/{session_id}")
async def get_history(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'get',
        f"{aiml_service_url}/sessions/history/{session_id}",
        user_id=user_id,
        params={'limit': limit, 'skip': skip}
    )

@router.post("/history/update/{session_id}")
async def update_history(
    request: Request,
    session_id: str,
    role: str = Body(...),
    content: str = Body(...),
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'post',
        f"{aiml_service_url}/sessions/history/update/{session_id}",
        user_id=user_id,
        json={'role': role, 'content': content}
    )

@router.get("/history/recent/{session_id}")
async def get_recent_history(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'get',
        f"{aiml_service_url}/sessions/history/recent/{session_id}",
        user_id=user_id,
        params={'limit': limit, 'skip': skip}
    )

@router.get("/get_all/{user_id}")
async def list_user_sessions(
    request: Request,
    user_id: str,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1,
    user: dict = Depends(get_current_user)
):
    return await forward_request(
        'get',
        f"{aiml_service_url}/sessions/get_all/{user_id}",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

@router.get("/get_by_agent/{agent_id}")
async def list_agent_sessions(
    request: Request,
    agent_id: str,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'get',
        f"{aiml_service_url}/sessions/get_by_agent/{agent_id}",
        user_id=user_id,
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

@router.get("/get/{session_id}")
async def get_session_details(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request(
        'get',
        f"{aiml_service_url}/sessions/get/{session_id}",
        user_id=user_id,
        params={'limit': limit, 'skip': skip}
    )

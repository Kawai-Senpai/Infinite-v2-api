from fastapi import APIRouter, HTTPException, Request, Body, Depends
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request
from errors.error_logger import log_exception_with_request   # <-- new import

router = APIRouter()

@router.post("/create")
async def create_session(
    request: Request,
    agent_id: str,
    max_context_results: int = 1,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'post',
            f"{aiml_service_url}/sessions/create",
            user_id=user_id,
            params={'agent_id': agent_id, 'max_context_results': max_context_results}
        )
    except Exception as e:
        log_exception_with_request(e, create_session, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{session_id}")
async def delete_session(
    request: Request,
    session_id: str,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'delete',
            f"{aiml_service_url}/sessions/delete/{session_id}",
            user_id=user_id
        )
    except Exception as e:
        log_exception_with_request(e, delete_session, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_history(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/history/{session_id}",
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
    except Exception as e:
        log_exception_with_request(e, get_history, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/update/{session_id}")
async def update_history(
    request: Request,
    session_id: str,
    role: str = Body(...),
    content: str = Body(...),
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'post',
            f"{aiml_service_url}/sessions/history/update/{session_id}",
            user_id=user_id,
            json={'role': role, 'content': content}
        )
    except Exception as e:
        log_exception_with_request(e, update_history, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/recent/{session_id}")
async def get_recent_history(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/history/recent/{session_id}",
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
    except Exception as e:
        log_exception_with_request(e, get_recent_history, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all")
async def list_user_sessions(
    request: Request,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/get_all/{user_id}",
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
    except Exception as e:
        log_exception_with_request(e, list_user_sessions, request)
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/get_by_agent/{agent_id}",
            user_id=user_id,
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
    except Exception as e:
        log_exception_with_request(e, list_agent_sessions, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{session_id}")
async def get_session_details(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/get/{session_id}",
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
    except Exception as e:
        log_exception_with_request(e, get_session_details, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/team/create")
async def create_team_session_route(
    request: Request,
    agent_ids: list = Body(...),
    max_context_results: int = 1,
    user: dict = Depends(get_current_user),
    session_type: str = "team"
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'post',
            f"{aiml_service_url}/sessions/team/create",
            user_id=user_id,
            json={
                "agent_ids": agent_ids,
                "max_context_results": max_context_results,
                "user_id": user_id,
                "session_type": session_type
            }
        )
    except Exception as e:
        log_exception_with_request(e, create_team_session_route, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team/history/{session_id}")
async def get_team_session_history_route(
    request: Request,
    session_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'get',
            f"{aiml_service_url}/sessions/team/history/{session_id}",
            user_id=user_id,
            params={'limit': limit, 'skip': skip}
        )
    except Exception as e:
        log_exception_with_request(e, get_team_session_history_route, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/team/history/update/{session_id}")
async def update_team_session_history_route(
    request: Request,
    session_id: str,
    agent_id: str = Body(None),
    role: str = Body(...),
    content: str = Body(...),
    summary: bool = False,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request(
            'post',
            f"{aiml_service_url}/sessions/team/history/update/{session_id}",
            user_id=user_id,
            json={
                "agent_id": agent_id,
                "role": role,
                "content": content,
                "user_id": user_id,
                "summary": summary
            }
        )
    except Exception as e:
        log_exception_with_request(e, update_team_session_history_route, request)
        raise HTTPException(status_code=500, detail=str(e))

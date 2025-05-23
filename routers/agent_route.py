from fastapi import APIRouter, HTTPException, Request, Body, Query, Depends
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request
from errors.error_logger import log_exception_with_request
from utilities.error_handler import handle_request_error

router = APIRouter()

@router.post("/create")
async def create_agent(
    request: Request,
    agent_type: str = Query(...),
    name: str = Query(...),
    body: dict = Body(...),  # Make this required since the other API expects it
    user: dict = Depends(get_current_user)
):
    try:
        valid_agent_types = ["public", "private"]
        if agent_type not in valid_agent_types:
            raise HTTPException(status_code=403, detail={
                "message": "Invalid agent type. Only public and private agents can be created.",
                "error": "Unauthorized agent type"
            })

        user_id = user.get("sub")
        # The other API expects user_id as a query parameter, not in the body
        url_params = {
            "user_id": user_id,
            "agent_type": agent_type,
            "name": name
        }
        # Change from '/agents/create' to '/agent/create' to match the other server's API
        return await forward_request('post', f"{aiml_service_url}/agents/create", params=url_params, json=body)
    except Exception as e:
        await handle_request_error(e, create_agent, request)

@router.get("/get_public")
async def get_public_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request(
            'get', 
            f"{aiml_service_url}/agents/get_public",
            params={
                'limit': limit, 
                'skip': skip, 
                'sort_by': sort_by, 
                'sort_order': sort_order,
                'user_id': user.get('sub')  # Add user_id to params
            }
        )
    except Exception as e:
        await handle_request_error(e, get_public_agents, request)

@router.delete("/delete/{agent_id}")
async def delete_agent(
    request: Request = None,
    agent_id: str = None,
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request('delete', f"{aiml_service_url}/agents/delete/{agent_id}",
            user_id=user_id
        )
    except Exception as e:
        await handle_request_error(e, delete_agent, request)

@router.get("/get_approved")
async def get_approved_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request(
            'get', 
            f"{aiml_service_url}/agents/get_approved",
            params={
                'limit': limit, 
                'skip': skip, 
                'sort_by': sort_by, 
                'sort_order': sort_order,
                'user_id': user.get('sub')  # Add user_id to params
            }
        )
    except Exception as e:
        await handle_request_error(e, get_approved_agents, request)

@router.get("/get_system")
async def get_system_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request(
            'get', 
            f"{aiml_service_url}/agents/get_system",
            params={
                'limit': limit, 
                'skip': skip, 
                'sort_by': sort_by, 
                'sort_order': sort_order,
                'user_id': user.get('sub')  # Add user_id to params
            }
        )
    except Exception as e:
        await handle_request_error(e, get_system_agents, request)

@router.get("/get_user_agents/{user_id}")
async def get_user_agents(
    request: Request,
    user_id: str,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = "created_at",
    sort_order: int = -1,
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request('get', f"{aiml_service_url}/agents/get_user_nonprivate/{user_id}",
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
        )
    except Exception as e:
        await handle_request_error(e, get_user_agents, request)

@router.get("/get_own")
async def get_private_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    try:
        user_id = user.get("sub")
        return await forward_request('get', f"{aiml_service_url}/agents/get_user/{user_id}",
            params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order},
            user_id=user_id
        )
    except Exception as e:
        await handle_request_error(e, get_private_agents, request)

@router.get("/get/{agent_id}")
async def get_agent_details(
    request: Request,
    agent_id: str,
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request('get', f"{aiml_service_url}/agents/get/{agent_id}",
            user_id=user.get('sub')
        )
    except Exception as e:
        await handle_request_error(e, get_agent_details, request)

@router.get("/tools")
async def get_available_tools(
    request: Request = None,
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request('get', f"{aiml_service_url}/agents/tools",
            user_id=user.get('sub')
        )
    except Exception as e:
        await handle_request_error(e, get_available_tools, request)

@router.put("/update/{agent_id}")
async def update_agent(
    request: Request,
    agent_id: str,
    body: dict = Body(...),
    user: dict = Depends(get_current_user)
):
    try:
        # Get the current agent details first
        current_agent = await forward_request('get', f"{aiml_service_url}/agents/get/{agent_id}", user_id=user.get('sub'))
        current_agent = current_agent.get('data', {})
        
        # Security checks
        if current_agent.get('agent_type') == 'system':
            raise HTTPException(status_code=403, detail={
                "message": "System agents cannot be modified.",
                "error": "Unauthorized modification attempt"
            })
            
        new_type = body.get('agent_type')
        current_type = current_agent.get('agent_type')
        
        # Prevent unauthorized type changes
        if new_type and new_type != current_type:
            # Prevent changing to system or approved
            if new_type in ['system', 'approved']:
                raise HTTPException(status_code=403, detail={
                    "message": "Cannot change agent type to system or approved.",
                    "error": "Unauthorized type change"
                })
                
            # Only allow changing to private
            if current_type != 'private' and new_type != 'private':
                raise HTTPException(status_code=403, detail={
                    "message": "Can only change agent type to private.",
                    "error": "Unauthorized type change"
                })

        # Forward the update request with the user's ID
        return await forward_request(
            'put',
            f"{aiml_service_url}/agents/update/{agent_id}",
            params={'user_id': user.get('sub')},
            json=body
        )

    except HTTPException:
        raise
    except Exception as e:
        await handle_request_error(e, update_agent, request)

@router.get("/search")
async def search_agent(
    request: Request,
    query: str = Query(..., description="Search term for agent names, capabilities or rules"),
    limit: int = Query(20),
    skip: int = Query(0),
    types: list = Query([], description="Agent types to filter (e.g., public, private, approved, system)"),
    sort_by: str = Query("created_at", description="Field to sort results by"),
    sort_order: int = Query(-1, description="Sort order (-1 for descending, 1 for ascending)"),
    user: dict = Depends(get_current_user)
):
    try:
        return await forward_request(
            'get',
            f"{aiml_service_url}/agents/search",
            params={
                'query': query,
                'limit': limit,
                'skip': skip,
                'types': types,
                'sort_by': sort_by,
                'sort_order': sort_order,
                'user_id': user.get('sub')  # Add user_id to params
            }
        )
    except Exception as e:
        await handle_request_error(e, search_agent, request)

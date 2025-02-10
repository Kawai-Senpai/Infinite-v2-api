from fastapi import APIRouter, HTTPException, Request, Body, Query, Depends
from fastapi.responses import JSONResponse
from keys.keys import aiml_service_url
from dependencies.auth import get_current_user
from utilities.forward import forward_request

router = APIRouter()

@router.post("/create")
async def create_agent(
    request: Request,
    agent_type: str = Query(...),
    name: str = Query(...),
    body: dict = Body(...),  # Make this required since the other API expects it
    user: dict = Depends(get_current_user)
):
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

@router.get("/get_public")
async def get_public_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    return await forward_request('get', f"{aiml_service_url}/agents/get_public",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

@router.delete("/delete/{agent_id}")
async def delete_agent(
    request: Request = None,
    agent_id: str = None,
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request('delete', f"{aiml_service_url}/agents/delete/{agent_id}",
        user_id=user_id
    )

@router.get("/get_approved")
async def get_approved_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    return await forward_request('get', f"{aiml_service_url}/agents/get_approved",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

@router.get("/get_system")
async def get_system_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    return await forward_request('get', f"{aiml_service_url}/agents/get_system",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

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
    return await forward_request('get', f"{aiml_service_url}/agents/get_user_nonprivate/{user_id}",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order}
    )

@router.get("/get_own")
async def get_private_agents(
    request: Request = None,
    limit: int = 20,
    skip: int = 0,
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1),
    user: dict = Depends(get_current_user)
):
    user_id = user.get("sub")
    return await forward_request('get', f"{aiml_service_url}/agents/get_user/{user_id}",
        params={'limit': limit, 'skip': skip, 'sort_by': sort_by, 'sort_order': sort_order},
        user_id=user_id
    )

@router.get("/get/{agent_id}")
async def get_agent_details(
    request: Request,
    agent_id: str,
    user: dict = Depends(get_current_user)
):
    return await forward_request('get', f"{aiml_service_url}/agents/get/{agent_id}",
        user_id=user.get('sub')
    )

@router.get("/tools")
async def get_available_tools(
    request: Request = None,
    user: dict = Depends(get_current_user)
):
    return await forward_request('get', f"{aiml_service_url}/agents/tools",
        user_id=user.get('sub')
    )

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
        raise HTTPException(status_code=500, detail={
            "message": "Internal Server Error while updating agent.",
            "error": str(e)
        })

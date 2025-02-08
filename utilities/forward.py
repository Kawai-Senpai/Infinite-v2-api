import httpx
from fastapi import HTTPException

async def forward_request(method: str, url: str, user_id: str = None, **kwargs):
    """
    A shared method to forward an HTTP request to the AIML service.
    """
    # If user_id is provided, add it to params
    if user_id:
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['user_id'] = user_id

    try:
        async with httpx.AsyncClient() as client:
            response = await getattr(client, method)(url, **kwargs)
            response.raise_for_status()
            # Check if the response content is empty
            if response.content:
                return response.json()
            else:
                # Return an empty dictionary if the response is empty
                return {}
    except httpx.HTTPStatusError as e:
        # Propagate the status code and message from the AIML service
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json()
        )
    except httpx.RequestError as e:
        # Network issues
        raise HTTPException(status_code=503, detail=str(e))

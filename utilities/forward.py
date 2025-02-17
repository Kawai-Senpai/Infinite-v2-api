import httpx
from fastapi import HTTPException
from json.decoder import JSONDecodeError  # new import
from bson import ObjectId  # new import
import asyncio  # new import

async def forward_request(method: str, url: str, user_id: str = None, **kwargs):
    """
    A shared method to forward an HTTP request to the AIML service.
    """
    MAX_RETRIES = 3  # new constant
    DELAY_SECONDS = 1  # new constant

    # If user_id is provided, add it to params
    if user_id:
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['user_id'] = user_id

    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await getattr(client, method)(url, **kwargs)
                response.raise_for_status()
                # Check if the response content is empty
                if response.content:
                    data = response.json()
                    return convert_object_ids(data)  # convert ObjectIds
                else:
                    # Return an empty dictionary if the response is empty
                    return {}
        except httpx.ConnectError as e:
            if attempt == MAX_RETRIES - 1:
                raise HTTPException(status_code=503, detail=f"Service unreachable after {MAX_RETRIES} attempts: {e}")
            await asyncio.sleep(DELAY_SECONDS)
        except httpx.HTTPStatusError as e:
            # Include response text for better error details
            try:
                detail = f"{e} - Response: {e.response.text}"
            except (JSONDecodeError, ValueError):
                detail = e.response.text
            raise HTTPException(
                status_code=e.response.status_code,
                detail=detail
            )
        except httpx.RequestError as e:
            # Network issues
            raise HTTPException(status_code=503, detail=str(e))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

def convert_object_ids(obj):
    if isinstance(obj, dict):
        return {k: convert_object_ids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_object_ids(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

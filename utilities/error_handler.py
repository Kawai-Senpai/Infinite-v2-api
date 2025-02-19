from fastapi import HTTPException
import httpx
from errors.error_logger import log_exception_with_request

def should_log_error(status_code: int, error: Exception) -> bool:
    """Determine if an error should be logged based on type and status code"""
    if isinstance(error, (SyntaxError, TypeError, ValueError, AttributeError)):
        return True
    if status_code >= 500:  # Internal server errors
        return True
    return False

async def handle_request_error(e, route_func, request):
    """
    Handle errors from forwarded requests, preserving the original error details
    Only log internal errors and Python-specific errors
    """
    if isinstance(e, httpx.HTTPError):
        if hasattr(e, 'response') and e.response is not None:
            try:
                status_code = e.response.status_code
                error_detail = e.response.json()
            except:
                status_code = getattr(e.response, 'status_code', 500)
                error_detail = str(e)
            
            # Only log if it's an internal error
            if should_log_error(status_code, e):
                log_exception_with_request(e, route_func, request)
        else:
            status_code = 500
            error_detail = str(e)
            log_exception_with_request(e, route_func, request)  # Log if no response
    else:
        # For non-HTTP errors, determine if we should log
        is_internal_error = isinstance(e, (SyntaxError, TypeError, ValueError, AttributeError))
        if is_internal_error:
            log_exception_with_request(e, route_func, request)
        status_code = 500 if is_internal_error else 400
        error_detail = str(e)

    raise HTTPException(
        status_code=status_code,
        detail=error_detail
    )

from fastapi import APIRouter, HTTPException, Request, Query, Depends
from dependencies.auth import get_current_user
from keys.keys import aiml_service_url
from utilities.forward import forward_request
from utilities.s3_loader import generate_download_link, generate_unique_filename, generate_upload_url
import boto3
from errors.error_logger import log_exception_with_request   # <-- new import

router = APIRouter()

ALLOWED_FILE_TYPES = {
    'pdf': ['application/pdf'],
    'txt': ['text/plain'],
    'doc': ['application/msword'],
    'docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'webpage': ['text/html', 'text/url']
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@router.post("/upload/generate_url")
async def generate_upload_url_endpoint(
    request: Request,
    file_name: str = Query(...),
    file_type: str = Query(...),
    file_size: int = Query(...),
    agent_id: str = Query(...),
    user: dict = Depends(get_current_user)
):
    try:
        # Validate file type
        if file_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail=f"File type {file_type} not allowed")
        
        # Convert MB to bytes and validate
        file_size = file_size * 1024 * 1024
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB")

        # Check for duplicate file name
        existing_files = await forward_request(
            'get',
            f"{aiml_service_url}/files/files/all/{agent_id}",
            params={'user_id': user.get('sub')}
        )
        
        if existing_files.get('data'):
            for file in existing_files['data']:
                if file['filename'].lower() == file_name.lower():
                    raise HTTPException(status_code=409, detail={
                        "message": "File with this name already exists",
                        "existing_file_id": str(file['_id'])
                    })

        # Generate S3 key and presigned URL
        s3_key = f"files/{user.get('sub')}/{generate_unique_filename(file_name)}"
        return {
            "message": "Upload URL generated successfully",
            **generate_upload_url(file_name, s3_key)
        }
    except HTTPException:
        raise
    except Exception as e:
        log_exception_with_request(e, generate_upload_url_endpoint, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def process_file(
    request: Request,
    s3_key: str = Query(...),
    file_name: str = Query(...),
    file_type: str = Query(...),
    agent_id: str = Query(...),
    collection_index: int = Query(None),
    chunk_size: int = Query(3),
    overlap: int = Query(1),
    chunk_type: str = Query("sentence"),
    user: dict = Depends(get_current_user)
):
    """Start processing a file that's been uploaded to S3"""
    try:
        # Forward the request to AIML service with added S3 details
        response = await forward_request(
            'post',
            f"{aiml_service_url}/files/jobs/start",
            params={
                'file_name': file_name,
                'file_type': file_type,
                'agent_id': agent_id,
                'collection_index': collection_index,
                'chunk_size': chunk_size,
                'overlap': overlap,
                'chunk_type': chunk_type,
                'user_id': user.get('sub'),
                's3_bucket': 'infinite-v2-data',
                's3_key': s3_key
            }
        )
        
        return response
    except Exception as e:
        log_exception_with_request(e, process_file, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{file_id}")
async def get_download_url(
    request: Request,
    file_id: str,
    user: dict = Depends(get_current_user)
):
    """Generate a download URL for a file"""
    try:
        # Get file details from AIML service
        file_details = await forward_request(
            'get',
            f"{aiml_service_url}/files/files/get/{file_id}",
            params={'user_id': user.get('sub')}
        )
        
        if file_details.get('file_type') == 'webpage':
            return {
                "message": "Webpage URL retrieved",
                "url": file_details.get('url')
            }
        
        # Generate pre-signed URL for S3 file
        download_url = generate_download_link(
            file_details.get('s3_key'),
            bucket_name=file_details.get('s3_bucket', 'infinite-v2-data')
        )
        
        return {
            "message": "Download URL generated successfully",
            "download_url": download_url
        }
    except Exception as e:
        log_exception_with_request(e, get_download_url, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{file_id}")
async def delete_file(
    request: Request,
    file_id: str,
    user: dict = Depends(get_current_user)
):
    """Delete a file and its associated chunks with better error handling"""
    try:
        # First get file details
        file_details = await forward_request(
            'get',
            f"{aiml_service_url}/files/files/get/{file_id}",
            params={'user_id': user.get('sub')}
        )
        
        errors = []
        
        # Delete from AIML service first (this will handle chunk deletion)
        try:
            await forward_request(
                'delete',
                f"{aiml_service_url}/files/delete/{file_id}",
                params={'user_id': user.get('sub')}
            )
        except Exception as e:
            errors.append(f"Failed to delete from AIML service: {str(e)}")
        
        # If it's not a webpage, delete from S3
        if file_details.get('file_type') != 'webpage':
            try:
                s3_client = boto3.client('s3')
                s3_client.delete_object(
                    Bucket=file_details.get('s3_bucket', 'infinite-v2-data'),
                    Key=file_details.get('s3_key')
                )
            except Exception as e:
                errors.append(f"Failed to delete from S3: {str(e)}")
        
        if errors:
            return {
                "message": "File deletion partially completed with errors",
                "errors": errors
            }
        
        return {"message": "File deleted successfully"}
    except Exception as e:
        log_exception_with_request(e, delete_file, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/{agent_id}")
async def get_agent_files(
    request: Request,
    agent_id: str,
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    """Get all files for an agent"""
    try:
        return await forward_request(
            'get',
            f"{aiml_service_url}/files/files/all/{agent_id}",
            params={
                'user_id': user.get('sub'),
                'limit': limit,
                'skip': skip
            }
        )
    except Exception as e:
        log_exception_with_request(e, get_agent_files, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections/{agent_id}")
async def get_agent_collections(
    request: Request,
    agent_id: str,
    user: dict = Depends(get_current_user)
):
    """Get all collections for an agent"""
    try:
        return await forward_request(
            'get',
            f"{aiml_service_url}/files/collections/all/{agent_id}",
            params={'user_id': user.get('sub')}
        )
    except Exception as e:
        log_exception_with_request(e, get_agent_collections, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections/files/{agent_id}/{collection_index}")
async def get_collection_files(
    request: Request,
    agent_id: str,
    collection_index: int,  # Changed from collection_id to collection_index
    limit: int = 20,
    skip: int = 0,
    user: dict = Depends(get_current_user)
):
    """Get all files in a collection using collection index"""
    try:
        return await forward_request(
            'get',
            f"{aiml_service_url}/files/collections/files/{agent_id}/{collection_index}",
            params={
                'user_id': user.get('sub'),
                'limit': limit,
                'skip': skip
            }
        )
    except Exception as e:
        log_exception_with_request(e, get_collection_files, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def validate_file(
    request: Request,
    file_name: str = Query(...),
    file_type: str = Query(...),
    file_size: int = Query(...),
    agent_id: str = Query(...),
    user: dict = Depends(get_current_user)
):
    """Validate file before upload"""
    try:
        issues = []
        
        # Check file type
        if file_type not in ALLOWED_FILE_TYPES:
            issues.append(f"File type {file_type} not allowed")
        
        # Convert file_size from MB to bytes for validation
        converted_size = file_size * 1024 * 1024
        if converted_size > MAX_FILE_SIZE:
            issues.append(f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB")
        
        # Check for duplicate
        existing_files = await forward_request(
            'get',
            f"{aiml_service_url}/files/files/all/{agent_id}",
            params={'user_id': user.get('sub')}
        )
        
        if existing_files.get('data'):
            for file in existing_files['data']:
                if file['filename'].lower() == file_name.lower():
                    issues.append("File with this name already exists")
                    break
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    except Exception as e:
        log_exception_with_request(e, validate_file, request)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}")
async def get_job_status(
    request: Request,
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """Get the status of a file processing job"""
    try:
        return await forward_request(
            'get',
            f"{aiml_service_url}/files/jobs/get/{job_id}"
        )
    except Exception as e:
        log_exception_with_request(e, get_job_status, request)
        raise HTTPException(status_code=500, detail=str(e))

# Files API Documentation

This document describes the Files API endpoints, which serve as a wrapper around the AIML service's file management system. It provides functionality for file uploads, downloads, and management with built-in validations and security.

## Overview

The Files API handles:
- File upload URL generation with pre-validation
- File processing initiation
- File downloads
- File deletion
- File listing and organization
- Collection management

## Authentication

All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## File Types and Limitations

### Supported File Types
```json
{
    "pdf": ["application/pdf"],
    "txt": ["text/plain"],
    "doc": ["application/msword"],
    "docx": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "webpage": ["text/html", "text/url"]
}
```

### Size Limits
- Maximum file size: 50MB

## Endpoints

### Generate Upload URL
`POST /files/upload/generate_url`

Generates a pre-signed S3 URL for file upload with validation checks.

#### Query Parameters
- `file_name` (required): Name of the file to upload
- `file_type` (required): Type of file (pdf, txt, doc, docx, webpage)
- `file_size` (required): Size of file in MB
- `agent_id` (required): ID of the agent to associate the file with

#### Response
```json
{
    "message": "Upload URL generated successfully",
    "upload_url": "https://s3-url...",
    "s3_key": "files/user123/filename-uuid.ext"
}
```

### Process File
`POST /files/process`

Initiates file processing after successful upload to S3.

#### Query Parameters
- `agent_id` (required): ID of the agent to associate the file with
- `s3_key` (required): S3 key of the uploaded file
- `file_name` (required): Original file name
- `file_type` (required): File type
- `collection_index` (required): Index of the collection to store the file in
- `chunk_size` (optional, default: 3): Number of sentences per chunk
- `overlap` (optional, default: 1): Number of overlapping sentences between chunks
- `chunk_type` (optional, default: "sentence"): Chunking method ("sentence" or "character")

#### Response
```json
{
    "message": "File processing started successfully",
    "job_id": "job123"
}
```

### Get Download URL
`GET /files/download/{file_id}`

Generates a download URL for a file.

#### Path Parameters
- `file_id` (required): ID of the file to download

#### Response
```json
{
    "message": "Download URL generated successfully",
    "download_url": "https://s3-url..."
}
```

For webpage type:
```json
{
    "message": "Webpage URL retrieved",
    "url": "https://example.com"
}
```

### Delete File
`DELETE /files/delete/{file_id}`

Deletes a file and its associated chunks.

#### Path Parameters
- `file_id` (required): ID of the file to delete

#### Response
```json
{
    "message": "File deleted successfully"
}
```

### List Agent Files
`GET /files/files/{agent_id}`

Retrieves all files associated with an agent.

#### Query Parameters
- `limit` (optional, default: 20): Number of files to return
- `skip` (optional, default: 0): Number of files to skip

#### Response
```json
{
    "message": "Files retrieved successfully",
    "data": [
        {
            "id": "file123",
            "filename": "example.pdf",
            "file_type": "pdf",
            "uploaded_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### List Collections
`GET /files/collections/{agent_id}`

Retrieves all collections for an agent.

#### Response
```json
{
    "message": "Collections retrieved successfully",
    "data": [
        {
            "id": "collection123",
            "name": "Collection 1"
        }
    ]
}
```

### List Collection Files
`GET /files/collections/files/{agent_id}/{collection_id}`

Retrieves all files in a specific collection.

#### Query Parameters
- `limit` (optional, default: 20): Number of files to return
- `skip` (optional, default: 0): Number of files to skip

#### Response
```json
{
    "message": "Collection files retrieved successfully",
    "data": [
        {
            "id": "file123",
            "filename": "example.pdf",
            "file_type": "pdf",
            "uploaded_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Validate File
`POST /files/validate`

Validates file metadata before upload.

#### Query Parameters
- `file_name` (required): Name of the file
- `file_type` (required): Type of file
- `file_size` (required): Size of file in MB
- `agent_id` (required): ID of the agent

#### Response
```json
{
    "valid": true,
    "issues": []
}
```

### Get Job Status
`GET /files/jobs/{job_id}`

Retrieves the status of a file processing job.

#### Path Parameters
- `job_id` (required): ID of the processing job to check

#### Response
```json
{
    "message": "Job details retrieved successfully",
    "data": {
    }
}
```

Possible status values:
- `pending`: Job is queued
- `processing`: Job is currently being processed
- `completed`: Job finished successfully
- `failed`: Job failed with error

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

```json
{
    "detail": {
        "message": "Error description",
        "error": "Detailed error message"
    }
}
```

Common status codes:
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 409: Conflict (e.g., duplicate file name)
- 500: Internal Server Error

## File Processing Flow

1. Client requests upload URL via `/files/upload/generate_url`
2. Client uploads file to S3 using the pre-signed URL
3. Client initiates processing via `/files/process`
4. Server processes file (chunking, embedding, etc.)
5. File becomes available for use in the agent's knowledge base

## Security Considerations

- All endpoints require authentication
- File types are strictly validated
- File sizes are limited
- S3 pre-signed URLs expire quickly
- User permissions are checked for all operations
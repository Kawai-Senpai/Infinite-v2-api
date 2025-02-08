# infinite-v2-api

A wrapper API for the AIML microservice that handles authentication and provides a secure interface for managing agents, sessions, and chat functionalities.

## Quick Start

1. Base URL: `http://localhost:9000`

2. Authentication:
   - All endpoints except `/status` require authentication via Clerk
   - Include JWT in the `Authorization` header as a Bearer token:
   ```
   Authorization: Bearer <JWT_TOKEN>
   ```

## Documentation

Detailed API documentation is split into three main sections:

1. [Agents API](doc/agents.md) - Everything related to creating and managing AI agents
2. [Sessions API](doc/sessions.md) - Managing chat sessions and their history
3. [Chat API](doc/chat.md) - The core chat functionality for interacting with agents

## Error Handling

The API uses standard HTTP status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Missing/invalid token
- `403 Forbidden`: Unauthorized access
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Errors are returned in JSON format:
```json
{
  "message": "Error description",
  "error": "Detailed error message"
}
```

## Status Check

To verify the service is running:
```bash
curl http://localhost:9000/status
```

Response:
```json
{
  "message": "Service status retrieved successfully.",
  "server": "API",
  "time": "...",
  "mongodb": "up"
}
```

## Dependencies

### AIML Microservice

This API acts as a wrapper around the core AIML microservice which must be running on port 8000. The AIML service handles:

- Language model interactions
- Memory management
- RAG (Retrieval Augmented Generation)
- Tool execution
- Agent behaviors

Configuration:
- AIML Service URL: `http://localhost:8000`
- Required for all agent and chat operations
- Must be running before starting this API

## Development

To run the API:

1. Ensure the AIML service is running on port 8000
2. Start this API on port 9000
3. Test the connection:
```bash
curl http://localhost:9000/status
```


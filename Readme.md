#### infinite-v2-api Documentation

# Introduction

This document provides a comprehensive guide to the infinite-v2-api, a wrapper API for the AIML microservice. This API handles authentication and forwards requests to the AIML service, providing a secure and streamlined interface for managing agents, sessions, and chat functionalities.

# Base URL

The base URL for the API is: `http://localhost:9000`

# Authentication

All endpoints except `/status` require authentication via Clerk. Include a valid JWT in the `Authorization` header as a Bearer token.

Example:
```
Authorization: Bearer <JWT_TOKEN>
```

# Endpoints

## 1. Agent Endpoints

### 1.1 Create Agent

- **Endpoint:** `POST /agent/create`
- **Description:** Creates a new agent.
- **Authentication:** Required
- **Request Body:**
```json
{
  "agent_type": "...",
  "name": "...",
  "role": "...",
  "capabilities": [],
  "rules": [],
  "model_provider": "openai",
  "model": "gpt-4o",
  "max_history": 20,
  "tools": [],
  "num_collections": 1,
  "max_memory_size": 5
}
```
- **Response:**
```json
{
  "message": "Agent created successfully.",
  "agent_id": "..."
}
```

### 1.2 Get Public Agents

- **Endpoint:** `GET /agent/get_public`
- **Description:** Retrieves a list of public agents.
- **Authentication:** Required
- **Query Parameters:**
  - `limit`: Maximum number of agents to retrieve (default: 20).
  - `skip`: Number of agents to skip (default: 0).
- **Response:**
```json
{
  "message": "Public agents retrieved successfully.",
  "data": [...]
}
```

### 1.3 Delete Agent

- **Endpoint:** `DELETE /agent/delete/{agent_id}`
- **Description:** Deletes an agent.
- **Authentication:** Required
- **Path Parameters:**
  - `agent_id`: ID of the agent to delete.
- **Response:**
```json
{
  "message": "Agent '{agent_id}' deleted successfully."
}
```

### 1.4 Get Approved Agents

- **Endpoint:** `GET /agent/get_approved`
- **Description:** Retrieves a list of approved agents.
- **Authentication:** Required
- **Query Parameters:**
  - `limit`: Maximum number of agents to retrieve (default: 20).
  - `skip`: Number of agents to skip (default: 0).
- **Response:**
```json
{
  "message": "Approved agents retrieved successfully.",
  "data": [...]
}
```

### 1.5 Get System Agents

- **Endpoint:** `GET /agent/get_system`
- **Description:** Retrieves a list of system agents.
- **Authentication:** Required
- **Query Parameters:**
  - `limit`: Maximum number of agents to retrieve (default: 20).
  - `skip`: Number of agents to skip (default: 0).
- **Response:**
```json
{
  "message": "System agents retrieved successfully.",
  "data": [...]
}
```

### 1.6 Get User Agents

- **Endpoint:** `GET /agent/get_user/{user_id}`
- **Description:** Retrieves a list of agents for a specific user.
- **Authentication:** Required
- **Path Parameters:**
  - `user_id`: ID of the user.
- **Query Parameters:**
  - `limit`: Maximum number of agents to retrieve (default: 20).
  - `skip`: Number of agents to skip (default: 0).
  - `sort_by`: Field to sort by (default: created_at).
  - `sort_order`: Sort order (1 for ascending, -1 for descending, default: -1).
- **Response:**
```json
{
  "message": "User agents retrieved successfully.",
  "data": [...]
}
```

### 1.7 Get Agent Details

- **Endpoint:** `GET /agent/get/{agent_id}`
- **Description:** Retrieves details for a specific agent.
- **Authentication:** Required
- **Path Parameters:**
  - `agent_id`: ID of the agent.
- **Response:**
```json
{
  "message": "Agent details retrieved successfully.",
  "data": {...}
}
```

### 1.8 Get Available Tools

- **Endpoint:** `GET /agent/tools`
- **Description:** Retrieves a list of available tools.
- **Authentication:** Required
- **Response:**
```json
{
  "message": "Available tools retrieved successfully.",
  "data": [...]
}
```

## 2. Session Endpoints

### 2.1 Create Session

- **Endpoint:** `POST /session/create`
- **Description:** Creates a new chat session.
- **Authentication:** Required
- **Query Parameters:**
  - `agent_id`: ID of the agent for the session.
  - `max_context_results`: Maximum number of context results (default: 1).
- **Response:**
```json
{
  "message": "Chat session created successfully.",
  "session_id": "..."
}
```

### 2.2 Delete Session

- **Endpoint:** `DELETE /session/delete/{session_id}`
- **Description:** Deletes a chat session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session to delete.
- **Response:**
```json
{
  "message": "Chat session deleted successfully."
}
```

### 2.3 Get Session History

- **Endpoint:** `GET /session/history/{session_id}`
- **Description:** Retrieves the history of a chat session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session.
- **Query Parameters:**
  - `limit`: Maximum number of history items to retrieve (default: 20).
  - `skip`: Number of history items to skip (default: 0).
- **Response:**
```json
{
  "message": "Session history retrieved successfully.",
  "data": [...]
}
```

### 2.4 Update Session History

- **Endpoint:** `POST /session/history/update/{session_id}`
- **Description:** Updates the history of a chat session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session.
- **Request Body:**
```json
{
  "role": "user" or "assistant",
  "content": "..."
}
```
- **Response:**
```json
{
  "message": "Session history updated successfully."
}
```

### 2.5 Get Recent History

- **Endpoint:** `GET /session/history/recent/{session_id}`
- **Description:** Retrieves the recent history of a chat session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session.
- **Query Parameters:**
  - `limit`: Maximum number of history items to retrieve (default: 20).
  - `skip`: Number of history items to skip (default: 0).
- **Response:**
```json
{
  "message": "Recent session history retrieved successfully.",
  "data": [...]
}
```

### 2.6 Get All User Sessions

- **Endpoint:** `GET /session/get_all/{user_id}`
- **Description:** Retrieves all sessions for a user.
- **Authentication:** Required
- **Path Parameters:**
  - `user_id`: ID of the user.
- **Query Parameters:**
  - `limit`: Maximum number of sessions to retrieve (default: 20).
  - `skip`: Number of sessions to skip (default: 0).
  - `sort_by`: Field to sort by (default: created_at).
  - `sort_order`: Sort order (1 for ascending, -1 for descending, default: -1).
- **Response:**
```json
{
  "message": "User sessions retrieved successfully.",
  "data": [...]
}
```

### 2.7 Get Agent Sessions

- **Endpoint:** `GET /session/get_by_agent/{agent_id}`
- **Description:** Retrieves sessions for a specific agent.
- **Authentication:** Required
- **Path Parameters:**
  - `agent_id`: ID of the agent.
- **Query Parameters:**
  - `limit`: Maximum number of sessions to retrieve (default: 20).
  - `skip`: Number of sessions to skip (default: 0).
  - `sort_by`: Field to sort by (default: created_at).
  - `sort_order`: Sort order (1 for ascending, -1 for descending, default: -1).
- **Response:**
```json
{
  "message": "Agent sessions retrieved successfully.",
  "data": [...]
}
```

### 2.8 Get Session Details

- **Endpoint:** `GET /session/get/{session_id}`
- **Description:** Retrieves details for a specific session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session.
- **Response:**
```json
{
  "message": "Session details retrieved successfully.",
  "data": {...}
}
```

## 3. Chat Endpoints

### 3.1 Chat with Agent

- **Endpoint:** `POST /chat/agent/{session_id}`
- **Description:** Sends a message to an agent in a specific session.
- **Authentication:** Required
- **Path Parameters:**
  - `session_id`: ID of the session.
- **Query Parameters:**
  - `agent_id`: ID of the agent.
  - `stream`: Enable streaming response (default: false).
  - `use_rag`: Enable Retrieval-Augmented Generation (default: true).
- **Request Body:**
```json
{
  "message": "..."
}
```
- **Response (non-streaming):**
```json
{
  "message": "Chat completed successfully.",
  "response": "..."
}
```
- **Response (streaming):**
  - Returns a `text/event-stream` with chunks of the response.

## 4. Utility Endpoints

### 4.1 Status

- **Endpoint:** `GET /status`
- **Description:** Retrieves the service status.
- **Authentication:** Not Required
- **Response:**
```json
{
  "message": "Service status retrieved successfully.",
  "server": "API",
  "time": "...",
  "mongodb": "up" or "down"
}
```

# Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Unauthorized access.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: An unexpected error occurred.

Errors are returned in JSON format with a `message` and `error` field.

Example:
```json
{
  "message": "Failed to create session.",
  "error": "Agent ID is required."
}
```

# Usage Examples

## Creating an Agent

```bash
curl -X POST \
  http://localhost:9000/agent/create \
  -H 'Authorization: Bearer <JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "agent_type": "...",
    "name": "MyAgent",
    "role": "Helpful assistant"
  }'
```

## Chatting with an Agent (non-streaming)

```bash
curl -X POST \
  http://localhost:9000/chat/agent/{session_id}?agent_id={agent_id} \
  -H 'Authorization: Bearer <JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Hello, how are you?"
  }'
```

## Getting Session History

```bash
curl -X GET \
  http://localhost:9000/session/history/{session_id} \
  -H 'Authorization: Bearer <JWT_TOKEN>'
```


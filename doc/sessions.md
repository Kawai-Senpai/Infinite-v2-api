# Session API Documentation

This document provides detailed information about the Session API endpoints, including request parameters, request body, and required headers.

## Base URL

All API endpoints are relative to the base URL of your API.  Replace `your_api_base_url` with the actual base URL.

```
your_api_base_url/sessions
```

## Authentication

All endpoints require a valid JWT (JSON Web Token) in the `Authorization` header. The token must be prefixed with `Bearer `.

Example:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Create Session

*   **Endpoint:** `POST /create`
*   **Description:** Creates a new chat session.
*   **Request Parameters:**
    *   `agent_id` (required):  The ID of the agent for this session.  String.
    *   `max_context_results` (optional): The maximum number of context results to consider. Integer. Default is `1`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required):  Bearer JWT token.
*   **Example Request:**

    ```
    POST /create?agent_id=agent123&max_context_results=3
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and the `session_id`.

    ```json
    {
        "message": "Chat session created successfully.",
        "session_id": "session123"
    }
    ```

### 2. Delete Session

*   **Endpoint:** `DELETE /delete/{session_id}`
*   **Description:** Deletes an existing chat session.
*   **Request Parameters:**
    *   `session_id` (required): The ID of the session to delete. String.  Passed as a path parameter.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    DELETE /delete/session123
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message.

    ```json
    {
        "message": "Chat session deleted successfully."
    }
    ```

### 3. Get Session History

*   **Endpoint:** `GET /history/{session_id}`
*   **Description:** Retrieves the history of a chat session.
*   **Request Parameters:**
    *   `session_id` (required): The ID of the session to retrieve history for. String. Passed as a path parameter.
    *   `limit` (optional): The maximum number of history items to retrieve. Integer. Default is `20`.
    *   `skip` (optional): The number of history items to skip. Integer. Default is `0`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    GET /history/session123?limit=50&skip=10
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and the session history data.

    ```json
    {
        "message": "Session history retrieved successfully.",
        "data": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
    }
    ```

### 4. Update Session History

*   **Endpoint:** `POST /history/update/{session_id}`
*   **Description:** Updates the history of a chat session by adding a new message.
*   **Request Parameters:**
    *   `session_id` (required): The ID of the session to update. String. Passed as a path parameter.
*   **Request Body:**

    ```json
    {
        "role": "user" or "assistant",
        "content": "The message content"
    }
    ```
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    POST /history/update/session123
    Authorization: Bearer <your_jwt_token>
    Content-Type: application/json

    {
        "role": "user",
        "content": "What is the capital of France?"
    }
    ```
*   **Response:**
    *   Returns a JSON object containing a success message.

    ```json
    {
        "message": "Session history updated successfully."
    }
    ```

### 5. Get Recent History

*   **Endpoint:** `GET /history/recent/{session_id}`
*   **Description:** Retrieves the most recent history of a chat session.
*   **Request Parameters:**
    *   `session_id` (required): The ID of the session to retrieve recent history for. String. Passed as a path parameter.
    *   `limit` (optional): The maximum number of recent history items to retrieve. Integer. Default is `20`.
    *   `skip` (optional): The number of recent history items to skip. Integer. Default is `0`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    GET /history/recent/session123?limit=10
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and the recent session history data.

    ```json
    {
        "message": "Recent session history retrieved successfully.",
        "data": [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "Paris"}
        ]
    }
    ```

### 6. List User Sessions

*   **Endpoint:** `GET /get_all/{user_id}`
*   **Description:** Retrieves all chat sessions for a specific user.
*   **Request Parameters:**
    *   `user_id` (required): The ID of the user. String. Passed as a path parameter.
    *   `limit` (optional): The maximum number of sessions to retrieve. Integer. Default is `20`.
    *   `skip` (optional): The number of sessions to skip. Integer. Default is `0`.
    *   `sort_by` (optional): The field to sort the sessions by. String. Default is `"created_at"`.
    *   `sort_order` (optional): The sort order. Integer. `-1` for descending, `1` for ascending. Default is `-1`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    GET /get_all/user123?limit=30&sort_by=last_active&sort_order=1
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and a list of sessions.

    ```json
    {
        "message": "User sessions retrieved successfully.",
        "data": [
            {"session_id": "session1", "agent_id": "agent1", "created_at": "2024-01-01"},
            {"session_id": "session2", "agent_id": "agent2", "created_at": "2024-01-02"}
        ]
    }
    ```

### 7. List Agent Sessions

*   **Endpoint:** `GET /get_by_agent/{agent_id}`
*   **Description:** Retrieves all chat sessions for a specific agent.
*   **Request Parameters:**
    *   `agent_id` (required): The ID of the agent. String. Passed as a path parameter.
    *   `limit` (optional): The maximum number of sessions to retrieve. Integer. Default is `20`.
    *   `skip` (optional): The number of sessions to skip. Integer. Default is `0`.
    *   `sort_by` (optional): The field to sort the sessions by. String. Default is `"created_at"`.
    *   `sort_order` (optional): The sort order. Integer. `-1` for descending, `1` for ascending. Default is `-1`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    GET /get_by_agent/agent123?limit=30&sort_by=last_active&sort_order=1
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and a list of sessions.

    ```json
    {
        "message": "Agent sessions retrieved successfully.",
        "data": [
            {"session_id": "session1", "user_id": "user1", "created_at": "2024-01-01"},
            {"session_id": "session2", "user_id": "user2", "created_at": "2024-01-02"}
        ]
    }
    ```

### 8. Get Session Details

*   **Endpoint:** `GET /get/{session_id}`
*   **Description:** Retrieves details for a specific chat session.
*   **Request Parameters:**
    *   `session_id` (required): The ID of the session. String. Passed as a path parameter.
    *   `limit` (optional): The maximum number of related items to retrieve. Integer. Default is `20`.
    *   `skip` (optional): The number of related items to skip. Integer. Default is `0`.
*   **Request Body:** None
*   **Headers:**
    *   `Authorization` (required): Bearer JWT token.
*   **Example Request:**

    ```
    GET /get/session123?limit=50
    Authorization: Bearer <your_jwt_token>
    ```
*   **Response:**
    *   Returns a JSON object containing a success message and the session details.

    ```json
    {
        "message": "Session details retrieved successfully.",
        "data": {
            "session_id": "session123",
            "agent_id": "agent123",
            "user_id": "user123",
            "created_at": "2024-01-01"
        }
    }
    ```

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of a request. Common error codes include:

*   `400 Bad Request`: Indicates that the request was malformed or invalid.
*   `401 Unauthorized`: Indicates that the user is not authenticated or does not have permission to access the resource.
*   `403 Forbidden`: Indicates that the user does not have permission to access the resource.
*   `404 Not Found`: Indicates that the requested resource was not found.
*   `500 Internal Server Error`: Indicates that an unexpected error occurred on the server.

Error responses typically include a JSON object with a `message` and an optional `error` field providing more details about the error.

```json
{
    "message": "Failed to retrieve session history.",
    "error": "Session not found."
}
```
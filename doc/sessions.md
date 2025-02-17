# Session API Documentation

This document provides detailed information about the Session API endpoints, including request parameters, request body, and required headers.

## Base URL

All API endpoints are relative to the base URL of your API. Replace `your_api_base_url` with the actual base URL.

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

* **Endpoint:** `POST /create`
* **Description:** Creates a new chat session for a single agent.
* **Request Parameters:**
    * `agent_id` (required): The ID of the agent. (string)
    * `max_context_results` (optional): Maximum number of context results. (integer; default: 1)
* **Request Body:** None (parameters passed via query string)
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    POST /create?agent_id=agent123&max_context_results=3
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Chat session created successfully.",
        "session_id": "session123"
    }
    ```

### 2. Delete Session

* **Endpoint:** `DELETE /delete/{session_id}`
* **Description:** Deletes an existing chat session.
* **Request Parameters:**
    * `session_id` (required): The ID of the session to delete. (string; path parameter)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    DELETE /delete/session123
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Chat session deleted successfully."
    }
    ```

### 3. Get Session History

* **Endpoint:** `GET /history/{session_id}`
* **Description:** Retrieves the history of a chat session.
* **Request Parameters:**
    * `session_id` (required): The ID of the session. (string; path parameter)
    * `limit` (optional): Maximum number of history items. (integer; default: 20)
    * `skip` (optional): Number of history items to skip. (integer; default: 0)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /history/session123?limit=50&skip=10
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Session history retrieved successfully.",
        "data": {
            "history": [ ... ],
            "total": 100,
            "skip": 10,
            "limit": 50
        }
    }
    ```

### 4. Update Session History

* **Endpoint:** `POST /history/update/{session_id}`
* **Description:** Adds a new message to a chat session’s history.
* **Request Parameters:**
    * `session_id` (required): The ID of the session. (string; path parameter)
* **Request Body:**

    ```json
    {
        "role": "user" or "assistant",
        "content": "The message content"
    }
    ```

* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    POST /history/update/session123
    Authorization: Bearer <your_jwt_token>
    Content-Type: application/json

    {
        "role": "user",
        "content": "What is the capital of France?"
    }
    ```

* **Response:**

    ```json
    {
        "message": "Session history updated successfully."
    }
    ```

### 5. Get Recent Session History

* **Endpoint:** `GET /history/recent/{session_id}`
* **Description:** Retrieves the most recent portion of a chat session's history.
* **Request Parameters:**
    * `session_id` (required): The ID of the session. (string; path parameter)
    * `limit` (optional): Maximum number of recent history items. (integer; default: 20)
    * `skip` (optional): Number of recent history items to skip. (integer; default: 0)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /history/recent/session123?limit=10
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Recent session history retrieved successfully.",
        "data": {
            "history": [ ... ],
            "total": 100,
            "skip": 0,
            "limit": 10
        }
    }
    ```

### 6. List User Sessions

* **Endpoint:** `GET /get_all/{user_id}`
* **Description:** Retrieves all chat sessions for the authenticated user.
* **Request Parameters:**
    * `user_id` (required): The ID of the user. (string; path parameter)
    * `limit` (optional): Maximum number of sessions. (integer; default: 20)
    * `skip` (optional): Number of sessions to skip. (integer; default: 0)
    * `sort_by` (optional): Field to sort by (default: `"created_at"`).
    * `sort_order` (optional): Sort order: `-1` for descending, `1` for ascending. (default: -1)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /get_all/user123?limit=30&sort_by=last_active&sort_order=1
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "User sessions retrieved successfully.",
        "data": [ ... ]
    }
    ```

### 7. List Agent Sessions

* **Endpoint:** `GET /get_by_agent/{agent_id}`
* **Description:** Retrieves all chat sessions for a specific agent, with an optional user authorization check.
* **Request Parameters:**
    * `agent_id` (required): The ID of the agent. (string; path parameter)
    * `limit` (optional): Maximum number of sessions. (integer; default: 20)
    * `skip` (optional): Number of sessions to skip. (integer; default: 0)
    * `sort_by` (optional): Field to sort by (default: `"created_at"`).
    * `sort_order` (optional): Sort order: `-1` for descending, `1` for ascending. (default: -1)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /get_by_agent/agent123?limit=30&sort_by=last_active&sort_order=1
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Agent sessions retrieved successfully.",
        "data": [ ... ]
    }
    ```

### 8. Get Session Details

* **Endpoint:** `GET /get/{session_id}`
* **Description:** Retrieves detailed information about a specific chat session.
* **Request Parameters:**
    * `session_id` (required): The ID of the session. (string; path parameter)
    * `limit` (optional): Maximum number of related items. (integer; default: 20)
    * `skip` (optional): Number of related items to skip. (integer; default: 0)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /get/session123?limit=50
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Session details retrieved successfully.",
        "data": {
            "session_id": "session123",
            "agent_id": "agent123",
            "user_id": "user123",
            "created_at": "2024-01-01",
            "history": [ ... ]
        }
    }
    ```

### 9. Create Team Session

* **Endpoint:** `POST /team/create`
* **Description:** Creates a new team chat session for multiple agents.
* **Request Parameters:** None (data provided in JSON body)
* **Request Body:**

    ```json
    {
        "agent_ids": ["agent1", "agent2"],
        "max_context_results": 1,
        "user_id": "user123",
        "session_type": "team"  // Other valid values: "team-managed", "team-flow" ; all spported: ["team", "team-managed", "team-flow"]
    }
    ```

* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    POST /team/create
    Authorization: Bearer <your_jwt_token>
    Content-Type: application/json

    {
        "agent_ids": ["agent1", "agent2"],
        "max_context_results": 1,
        "user_id": "user123",
        "session_type": "team"
    }
    ```

* **Response:**

    ```json
    {
        "message": "Team session created successfully.",
        "session_id": "teamSession123"
    }
    ```

### 10. Get Team Session History

* **Endpoint:** `GET /team/history/{session_id}`
* **Description:** Retrieves the history of a team session, including messages from all participating agents.
* **Request Parameters:**
    * `session_id` (required): The team session’s ID. (string; path parameter)
    * `limit` (optional): Maximum number of history items. (integer; default: 20)
    * `skip` (optional): Number of history items to skip. (integer; default: 0)
* **Request Body:** None
* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    GET /team/history/teamSession123?limit=30&skip=0
    Authorization: Bearer <your_jwt_token>
    ```

* **Response:**

    ```json
    {
        "message": "Team session history retrieved successfully.",
        "data": {
            "history": [ ... ],
            "total": 50,
            "skip": 0,
            "limit": 30
        }
    }
    ```

### 11. Update Team Session History

* **Endpoint:** `POST /team/history/update/{session_id}`
* **Description:** Adds a new message to the history of a team session. Optionally, a summary message can be added.
* **Request Parameters:**
    * `session_id` (required): The team session’s ID. (string; path parameter)
* **Request Body:**

    ```json
    {
        "agent_id": "agent1",       // Optional; if provided, will include the agent name from team session info.
        "role": "user" or "assistant",
        "content": "The message content",
        "summary": false            // Optional; defaults to false. Set true for summary messages.
    }
    ```

* **Headers:** `Authorization: Bearer <your_jwt_token>`
* **Example Request:**

    ```
    POST /team/history/update/teamSession123
    Authorization: Bearer <your_jwt_token>
    Content-Type: application/json

    {
        "agent_id": "agent1",
        "role": "assistant",
        "content": "Here is the update on the current team task.",
        "summary": false
    }
    ```

* **Response:**

    ```json
    {
        "message": "Team session history updated successfully."
    }
    ```

## Error Handling

The API returns standard HTTP status codes to indicate the result of a request. Common status codes include:

* `400 Bad Request`: The request is malformed or invalid.
* `401 Unauthorized`: The request is not authenticated.
* `403 Forbidden`: The user does not have permission to perform the action.
* `404 Not Found`: The specified resource could not be found.
* `500 Internal Server Error`: An unexpected server error occurred.

Error responses are in the following JSON format:

```json
{
    "message": "Description of the error.",
    "error": "Detailed error message if available."
}
```

# Notes

* Ensure that ObjectId conversions are properly handled on the backend.
* For team sessions, the user creating the session is stored and checked for permissions.
* The endpoints prefixed with `/team` are designed to handle multi-agent conversations.
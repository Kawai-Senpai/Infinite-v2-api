# Agent API Documentation

This document provides detailed information about the Agent API endpoints, including request parameters, body, headers, and response formats.

## Base URL

The base URL for all Agent API endpoints is: `[Your API Base URL]`

## Authentication

All endpoints require authentication via a JWT (JSON Web Token) in the `Authorization` header. The token must be prefixed with `Bearer `.

Example:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Create Agent

*   **URL:** `/agents/create`
*   **Method:** `POST`
*   **Description:** Creates a new agent.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Query Parameters:**
    *   `agent_type` (string): Required. The type of agent to create (e.g., "system", "user").
    *   `name` (string): Required. The name of the agent.

    **Request Body (JSON):**
    ```json
    {
        "role": "string",          // Optional. The role of the agent.
        "capabilities": [],        // Optional. An array of strings representing the agent's capabilities.
        "rules": [],               // Optional. An array of strings representing the agent's rules.
        "model_provider": "string",// Optional. The model provider (e.g., "openai"). Default: "openai".
        "model": "string",         // Optional. The model to use (e.g., "gpt-4o"). Default: "gpt-4o".
        "max_history": integer,    // Optional. The maximum number of messages to store in the agent's history. Default: 20.
        "tools": [],               // Optional. An array of strings representing the tools the agent can use.
        "num_collections": integer, // Optional. The number of memory collections to create. Default: 1.
        "max_memory_size": integer  // Optional. The maximum size of the agent's memory. Default: 5.
    }
    ```

    **Response (Success):**
    ```json
    {
        "message": "Agent created successfully.",
        "agent_id": "string"  // The ID of the newly created agent.
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Failed to create agent.",
        "error": "string"  // Error message.
    }
    ```

### 2. Get Public Agents

*   **URL:** `/agents/get_public`
*   **Method:** `GET`
*   **Description:** Retrieves a list of public agents.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Query Parameters:**
    *   `limit` (integer): Optional. The maximum number of agents to return. Default: 20.
    *   `skip` (integer): Optional. The number of agents to skip. Default: 0.
    *   `sort_by` (string): Optional. The field to sort by (e.g., "created_at"). Default: "created_at".
    *   `sort_order` (integer): Optional. The sort order (-1 for descending, 1 for ascending). Default: -1.

    **Response (Success):**
    ```json
    {
        "message": "Public agents retrieved successfully.",
        "data": [
            // Array of agent objects
            {
                "id": "string",
                "name": "string",
                "agent_type": "string",
                "created_at": "string",
                "updated_at": "string"
                // ... other agent properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Internal Server Error while retrieving public agents.",
        "error": "string"  // Error message.
    }
    ```

### 3. Delete Agent

*   **URL:** `/agents/delete/{agent_id}`
*   **Method:** `DELETE`
*   **Description:** Deletes an agent.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Path Parameters:**
    *   `agent_id` (string): Required. The ID of the agent to delete.

    **Response (Success):**
    ```json
    {
        "message": "Agent '{agent_id}' deleted successfully."
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Failed to delete agent.",
        "error": "string"  // Error message.
    }
    ```

### 4. Get Approved Agents

*   **URL:** `/agents/get_approved`
*   **Method:** `GET`
*   **Description:** Retrieves a list of approved agents.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Query Parameters:**
    *   `limit` (integer): Optional. The maximum number of agents to return. Default: 20.
    *   `skip` (integer): Optional. The number of agents to skip. Default: 0.
    *   `sort_by` (string): Optional. The field to sort by (e.g., "created_at"). Default: "created_at".
    *   `sort_order` (integer): Optional. The sort order (-1 for descending, 1 for ascending). Default: -1.

    **Response (Success):**
    ```json
    {
        "message": "Approved agents retrieved successfully.",
        "data": [
            // Array of agent objects
            {
                "id": "string",
                "name": "string",
                "agent_type": "string",
                "created_at": "string",
                "updated_at": "string"
                // ... other agent properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Internal Server Error while retrieving approved agents.",
        "error": "string"  // Error message.
    }
    ```

### 5. Get System Agents

*   **URL:** `/agents/get_system`
*   **Method:** `GET`
*   **Description:** Retrieves a list of system agents.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Query Parameters:**
    *   `limit` (integer): Optional. The maximum number of agents to return. Default: 20.
    *   `skip` (integer): Optional. The number of agents to skip. Default: 0.
    *   `sort_by` (string): Optional. The field to sort by (e.g., "created_at"). Default: "created_at".
    *   `sort_order` (integer): Optional. The sort order (-1 for descending, 1 for ascending). Default: -1.

    **Response (Success):**
    ```json
    {
        "message": "System agents retrieved successfully.",
        "data": [
            // Array of agent objects
            {
                "id": "string",
                "name": "string",
                "agent_type": "string",
                "created_at": "string",
                "updated_at": "string"
                // ... other agent properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Internal Server Error while retrieving system agents.",
        "error": "string"  // Error message.
    }
    ```

### 6. Get User Agents (Non-Private)

*   **URL:** `/agents/get_user_agents/{user_id}`
*   **Method:** `GET`
*   **Description:** Retrieves a list of non-private agents for a specific user.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Path Parameters:**
    *   `user_id` (string): Required. The ID of the user.

    **Query Parameters:**
    *   `limit` (integer): Optional. The maximum number of agents to return. Default: 20.
    *   `skip` (integer): Optional. The number of agents to skip. Default: 0.
    *   `sort_by` (string): Optional. The field to sort by (e.g., "created_at"). Default: "created_at".
    *   `sort_order` (integer): Optional. The sort order (-1 for descending, 1 for ascending). Default: -1.

    **Response (Success):**
    ```json
    {
        "message": "User non-private agents retrieved successfully.",
        "data": [
            // Array of agent objects
            {
                "id": "string",
                "name": "string",
                "agent_type": "string",
                "created_at": "string",
                "updated_at": "string"
                // ... other agent properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Internal Server Error while retrieving user non-private agents.",
        "error": "string"  // Error message.
    }
    ```

### 7. Get Own Agents

*   **URL:** `/agents/get_own`
*   **Method:** `GET`
*   **Description:** Retrieves a list of own agents for the authenticated user.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Query Parameters:**
    *   `limit` (integer): Optional. The maximum number of agents to return. Default: 20.
    *   `skip` (integer): Optional. The number of agents to skip. Default: 0.
    *   `sort_by` (string): Optional. The field to sort by (e.g., "created_at"). Default: "created_at".
    *   `sort_order` (integer): Optional. The sort order (-1 for descending, 1 for ascending). Default: -1.

    **Response (Success):**
    ```json
    {
        "message": "User agents retrieved successfully.",
        "data": [
            // Array of agent objects
            {
                "id": "string",
                "name": "string",
                "agent_type": "string",
                "created_at": "string",
                "updated_at": "string"
                // ... other agent properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Internal Server Error while retrieving user agents.",
        "error": "string"  // Error message.
    }
    ```

### 8. Get Agent Details

*   **URL:** `/agents/get/{agent_id}`
*   **Method:** `GET`
*   **Description:** Retrieves details for a specific agent.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Path Parameters:**
    *   `agent_id` (string): Required. The ID of the agent.

    **Response (Success):**
    ```json
    {
        "message": "Agent details retrieved successfully.",
        "data": {
            "id": "string",
            "name": "string",
            "agent_type": "string",
            "created_at": "string",
            "updated_at": "string"
            // ... other agent properties
        }
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Failed to retrieve agent details.",
        "error": "string"  // Error message.
    }
    ```

### 9. Get Available Tools

*   **URL:** `/agents/tools`
*   **Method:** `GET`
*   **Description:** Retrieves a list of available tools.

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Response (Success):**
    ```json
    {
        "message": "Available tools retrieved successfully.",
        "data": [
            // Array of tool objects
            {
                "name": "string",
                "description": "string"
                // ... other tool properties
            }
        ]
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Failed to retrieve available tools.",
        "error": "string"  // Error message.
    }
    ```

### 10. Update Agent

*   **URL:** `/agents/update/{agent_id}`
*   **Method:** `PUT`
*   **Description:** Updates an existing agent's details. Has special restrictions on type changes:
    - System agents cannot be modified
    - Cannot change any agent to type "system" or "approved"
    - Can only change public/approved agents to "private"

    **Headers:**
    *   `Authorization`: Required. JWT token for authentication.

    **Path Parameters:**
    *   `agent_id` (string): Required. The ID of the agent to update.

    **Request Body (JSON):**
    ```json
    {
        "name": "string",         // Optional. New name for the agent
        "role": "string",         // Optional. New role for the agent
        "capabilities": [],       // Optional. New array of capabilities
        "rules": [],             // Optional. New array of rules
        "agent_type": "string"   // Optional. New type (restrictions apply)
    }
    ```

    **Response (Success):**
    ```json
    {
        "message": "Agent updated successfully.",
        "success": true
    }
    ```

    **Response (Error):**
    ```json
    {
        "message": "Failed to update agent.",
        "error": "string"  // Error message detailing why the update failed
    }
    ```

    **Possible Error Messages:**
    - "System agents cannot be modified."
    - "Cannot change agent type to system or approved."
    - "Can only change agent type to private."
    - "Not authorized to update this agent."
    - "Agent not found."
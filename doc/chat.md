# Chat API Documentation

This document describes the Chat API endpoint, which acts as a wrapper around the core AIML service. It provides details on how to use the endpoint, including required parameters, request body format, headers, and expected responses.

## Endpoint

`POST /chat/agent/{session_id}`

## Description

This endpoint allows users to interact with an AI agent by sending messages and receiving responses. It supports both streaming and non-streaming modes.

## Parameters

### Path Parameters

-   `session_id` (required): A unique identifier for the chat session. This allows the agent to maintain context across multiple messages.

### Query Parameters

-   `agent_id` (required): The identifier of the AI agent to be used for the chat.
-   `stream` (optional, default: `False`): A boolean value indicating whether to use streaming mode. If `True`, the response will be streamed as `text/event-stream`.
-   `use_rag` (optional, default: `True`): A boolean value indicating whether to use Retrieval-Augmented Generation (RAG).
-   `include_rich_response` (optional, default: `True`): A boolean value indicating whether to include additional metadata (tool results, tools used, tools not used, and memories used) in the response.
-   `user_id` (required): The identifier of the user.

### Headers

-   `Authorization` (required): A JWT token used for authentication. The token must be in the format `Bearer <token>`.

## Request Body

The request body must be a JSON object containing the following field:

-   `message` (required): The message to be sent to the AI agent.  This cannot be empty or consist only of whitespace.

Example:

```json
{
    "message": "Hello, how are you?"
}
```

## Example Usage

### Streaming Mode

To initiate a streaming chat, set the `stream` query parameter to `True`.

```bash
curl -X POST \
  "http://your-api-url/chat/agent/67a7713cc2cd96464c5c0675?agent_id=67a76191085410c37086004a&stream=True&use_rag=False" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{ "message": "Tell me a joke." }'
```

### Non-Streaming Mode

To initiate a non-streaming chat, either omit the `stream` query parameter or set it to `False`.

```bash
curl -X POST \
  "http://your-api-url/chat/agent/67a7713cc2cd96464c5c0675?agent_id=67a76191085410c37086004a&stream=False&use_rag=True" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{ "message": "What is the capital of France?" }'
```

## Responses

### Success (Non-Streaming)

When `include_rich_response` is enabled, the JSON response includes additional metadata keys:

```json
{
    "message": "Chat completed successfully.",
    "response": "The capital of France is Paris.",
    "tool_results": [ ... ],
    "tools_used": [ ... ],
    "tools_not_used": [ ... ],
    "memories_used": [ ... ]
}
```

### Success (Streaming)

The server will stream the response as `text/event-stream`. Each chunk of the response will be sent as a separate event.

### Error

```json
{
    "message": "Chat request failed.",
    "error": "Message is required and cannot be empty"
}
```

```json
{
    "message": "Unauthorized",
    "error": "Invalid token"
}
```

## Notes

-   Ensure that the JWT token provided in the `Authorization` header is valid and not expired.
-   The `agent_id` must correspond to a valid AI agent configured in the AIML service.
-   The `session_id` should be unique for each chat session to maintain context.
-   If `stream` is set to `True`, the response will be streamed, and the client should handle the `text/event-stream` format.
-   If `use_rag` is set to `True`, the agent will use Retrieval-Augmented Generation to enhance its responses.

## Team Chat API Documentation

### Endpoint

`POST /chat/team/{session_id}`

### Description

This endpoint enables multi-agent team chat functionality. It supports three different team chat modes:
- Basic team chat (sequential responses from all agents)
- Managed team chat (order determined by a manager agent)
- Flow-based team chat (dynamic agent selection based on context)

The mode is determined by the session's type, which is set when creating the team session ("team", "team-managed", or "team-flow").

### Parameters

#### Path Parameters
- `session_id` (required): Unique identifier for the team chat session

#### Query Parameters
- `stream` (optional, default: `False`): Enable streaming responses
- `use_rag` (optional, default: `True`): Enable Retrieval-Augmented Generation
- `include_rich_response` (optional, default: `True`): Include metadata in responses

### Request Body

```json
{
    "message": "Your message here"
}
```

### Headers
- `Authorization` (required): Bearer token for authentication

### Responses

#### Non-Streaming Response Format

```json
{
    "responses": {
        "Agent Name 1": {
            "response": "Agent 1's response",
            "tool_results": [...],
            "tools_used": [...],
            "tools_not_used": [...],
            "memories_used": [...],
            "context_results": [...]
        },
        "Agent Name 2": {
            "response": "Agent 2's response",
            "tool_results": [...],
            "tools_used": [...],
            "tools_not_used": [...],
            "memories_used": [...],
            "context_results": [...]
        },
        "summary": "A summary of the conversation"
    },
    "conversation": "[Agent Name 1]: Agent 1's response\n[Agent Name 2]: Agent 2's response\nSummary: A summary of the conversation"
}
```

#### Streaming Response Format

The streaming response is formatted as text/event-stream with the following structure:
```
[agent <agent_id>]
<agent response content>
[metadata]={"tool_results": [...], "tools_used": [...], ...}

[agent <next_agent_id>]
<next agent response content>
[metadata]={"tool_results": [...], "tools_used": [...], ...}

[summary]
<conversation summary>
```

### Team Session Types

#### Basic Team Chat ("team")
- All agents respond in sequence
- Each agent sees previous agents' responses
- Conversation ends with a summary

#### Managed Team Chat ("team-managed")
- A management layer determines the optimal order of agent responses
- Order is based on agent roles and message content
- More structured than basic team chat
- Ends with a summary

#### Flow Team Chat ("team-flow")
- Dynamic agent selection based on conversation context
- Agents are selected one at a time based on their relevance
- Conversation flows naturally between agents
- Has a maximum step limit to prevent infinite loops
- Ends with a summary

### Error Responses

```json
{
    "detail": "Session not found"
}
```

```json
{
    "detail": "Not a team session"
}
```

### Example Usage

#### Basic Request
```bash
curl -X POST \
  "http://your-api-url/chat/team/67a7713cc2cd96464c5c0675" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the pros and cons of using microservices?"}'
```

#### Streaming Request
```bash
curl -X POST \
  "http://your-api-url/chat/team/67a7713cc2cd96464c5c0675?stream=true" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain the benefits of containerization."}'
```

### Notes

1. The team session type must be set when creating the session and cannot be changed during chat.
2. Each agent in the team has access to:
   - The original user message
   - Previous agents' responses
   - Context from RAG (if enabled)
   - Their individual tools and memories
3. The summary is automatically generated after all agents have responded.
4. In flow mode, there's a maximum limit of 50 steps to prevent infinite loops.
5. Rich responses include metadata about tools used, memory accessed, and RAG results.
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

```json
{
    "message": "Chat completed successfully.",
    "response": "The capital of France is Paris."
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
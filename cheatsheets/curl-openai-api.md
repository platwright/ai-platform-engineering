# curl OpenAI-Compatible API Cheatsheet

## Health Check

```bash
curl http://localhost:8001/health
```

## Chat Completion (Basic)

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "your-model-name",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain what a KV cache is."}
    ],
    "max_tokens": 200,
    "temperature": 0.7
  }'
```

## Chat Completion (Streaming)

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -N \
  -d '{
    "model": "your-model-name",
    "messages": [{"role": "user", "content": "Count to 5 slowly."}],
    "stream": true
  }'
```

## Chat Completion With JSON Mode

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "your-model-name",
    "messages": [
      {"role": "system", "content": "Return a JSON object with fields: topic and summary."},
      {"role": "user", "content": "Summarize what RAG is."}
    ],
    "response_format": {"type": "json_object"},
    "max_tokens": 200
  }'
```

## Embeddings

```bash
curl -X POST http://localhost:8001/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "text-embedding-3-small",
    "input": "Platform engineers build AI platforms."
  }'
```

## List Available Models

```bash
curl http://localhost:8001/v1/models \
  -H "Authorization: Bearer $API_KEY" \
  | jq '.data[].id'
```

## Extract Token Usage From Response

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{ "model": "...", "messages": [{"role": "user", "content": "Hi"}] }' \
  | jq '.usage'
```

## Extract Only The Response Text

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{ "model": "...", "messages": [{"role": "user", "content": "Hi"}] }' \
  | jq -r '.choices[0].message.content'
```

## Chat With Tool Definitions

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "your-model-name",
    "messages": [{"role": "user", "content": "What is the current error rate?"}],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_metrics",
          "description": "Get current platform metrics",
          "parameters": {
            "type": "object",
            "properties": {
              "metric": {"type": "string", "enum": ["error_rate", "latency_p99"]}
            },
            "required": ["metric"]
          }
        }
      }
    ],
    "tool_choice": "auto"
  }'
```

## Environment Variables For Quick Scripts

```bash
export API_KEY="your-api-key"
export API_BASE="http://localhost:8001"
export MODEL="your-model-name"

# Then use:
curl -X POST $API_BASE/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{\"model\": \"$MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]}"
```

## Measuring TTFT With curl

```bash
# Time to first byte approximates TTFT for streaming responses
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -N \
  -w "\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -o /dev/null \
  -d '{ "model": "...", "messages": [...], "stream": true }'
```

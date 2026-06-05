# Streaming Responses

## At a Glance
| | |
|---|---|
| **Category** | Interaction Pattern / UX Optimization |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours for implementation, weeks for production-grade patterns |
| **Prerequisites** | Understanding of async programming, HTTP protocols, LLM APIs, event-driven architectures |

## One-Sentence Summary
Streaming responses is the pattern where AI agents and LLMs return output incrementally as tokens are generated—sending the first words within 200-500 milliseconds and continuing word-by-word until complete—instead of making users wait 5-30 seconds staring at loading spinners for fully buffered responses, transforming perceived latency from "frustratingly slow" to "feels instant and responsive" even though total time remains similar.

## Why This Matters to You
When you build AI agent interfaces in 2026, streaming responses are the difference between applications users love and applications users abandon. Without streaming, users wait in silence: query submitted → 10 second spinner → full response appears. Users cannot gauge progress, don't know if the system crashed, and perceive the experience as "slow" even for 5-second responses. With streaming, users see immediate feedback: query submitted → first words appear in 300ms → continuous word-by-word output → completion in 5 seconds. The total time is nearly identical (5.3s vs 5s), but perceived latency drops dramatically—users feel the system is "thinking out loud" and responding instantly. This perception matters enormously: studies show users tolerate 20+ second streaming responses but abandon 5+ second buffered responses. Streaming also enables critical UX features: users can read while generation continues (parallelizing human processing with AI generation), cancel mid-generation when they've seen enough (saving 70% of completion costs), and detect errors or off-topic responses early (stopping hallucinations before completion). For long-form content (essays, code, reports), streaming is essential—users won't wait 60 seconds for 2000 tokens when they could start reading at 500ms. But streaming adds complexity: frontend must handle partial updates, backend needs async/generator patterns, errors occur mid-stream requiring special handling, and caching becomes harder (what do you cache when responses arrive incrementally?). Understanding streaming implementation—Server-Sent Events (SSE), async generators, token buffering strategies, error propagation, and cancellation handling—determines whether your agent interfaces feel modern and responsive or outdated and frustrating. In 2026, streaming is expected UX, not optional enhancement; users judge AI applications by responsiveness, and streaming is the primary technique delivering that responsiveness.

## The Core Idea
### What It Is
Streaming responses is an interaction pattern where the AI agent or LLM sends output incrementally in small chunks (typically individual tokens or small token groups) as they're generated, rather than buffering the complete response before sending. The client receives and displays these chunks progressively, showing users the response as it's being created.

**The Fundamental UX Problem:**

LLM generation takes time—typically 20-50 tokens/second for production models in 2026. A 500-token response takes 10-25 seconds to generate. Without streaming:

```
User submits query → [10-25 second blank screen] → Complete response appears
```

Users experience this as unresponsive, broken, or slow. They cannot:
- See progress
- Know if the system is working
- Read while waiting
- Cancel early if response is wrong
- Gauge how much longer they'll wait

With streaming:

```
User submits query → [300ms] → First tokens appear → Continuous word-by-word output → [10-25 seconds] → Complete
```

Users experience this as responsive and fast, even though total time is similar. They can:
- See immediate feedback (system is working)
- Read while generation continues
- Cancel anytime (saw enough or wrong direction)
- Gauge progress (halfway through, almost done)

**Technical Implementation:**

Streaming requires three components working together:

**1. LLM API Streaming Support:**

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def get_streaming_response(prompt: str):
    """
    Call OpenAI API with streaming enabled.
    
    Returns generator yielding token chunks.
    """
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,  # Enable streaming!
        temperature=0.7
    )
    
    # Iterate over chunks as they arrive
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            yield token

# Usage
prompt = "Explain how neural networks work in simple terms."

print("Response: ", end="", flush=True)
for token in get_streaming_response(prompt):
    print(token, end="", flush=True)  # Print each token immediately
print()  # Newline at end

# Output appears word-by-word as it's generated:
# Response: Neural networks are computational models inspired by...
```

**2. Backend Streaming Infrastructure (Server-Sent Events):**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from typing import AsyncGenerator

app = FastAPI()

async def generate_streaming_tokens(prompt: str) -> AsyncGenerator[str, None]:
    """
    Async generator for streaming tokens.
    
    Yields tokens as they're generated from LLM.
    """
    # Call LLM API with streaming
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    # Yield tokens in SSE format
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            
            # SSE format: "data: {token}\n\n"
            yield f"data: {token}\n\n"
    
    # Signal completion
    yield "data: [DONE]\n\n"

@app.post("/api/stream")
async def stream_response(query: dict):
    """
    Streaming endpoint using Server-Sent Events.
    
    Client connects, receives tokens as they're generated.
    """
    prompt = query.get("prompt", "")
    
    return StreamingResponse(
        generate_streaming_tokens(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

# Client connects to /api/stream and receives SSE stream
```

**3. Frontend Streaming Consumption:**

```javascript
// JavaScript/TypeScript client consuming SSE stream

async function streamResponse(prompt) {
    const response = await fetch('/api/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    let responseElement = document.getElementById('response');
    responseElement.textContent = '';  // Clear previous
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
                break;
            }
            
            // Decode chunk and extract tokens
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const token = line.slice(6);
                    
                    if (token === '[DONE]') {
                        console.log('Stream complete');
                        return;
                    }
                    
                    // Append token to display
                    responseElement.textContent += token;
                }
            }
        }
    } catch (error) {
        console.error('Streaming error:', error);
        responseElement.textContent += '\n\n[Error: Stream interrupted]';
    }
}

// Usage
const userPrompt = "Explain quantum computing simply";
streamResponse(userPrompt);

// UI updates word-by-word as tokens arrive
```

**Advanced: Streaming with Markdown Rendering:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from typing import AsyncGenerator

async def generate_streaming_with_metadata(
    prompt: str
) -> AsyncGenerator[str, None]:
    """
    Stream tokens with metadata for rich rendering.
    
    Each chunk includes: token, cumulative text, metadata.
    """
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    cumulative_text = ""
    token_count = 0
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            cumulative_text += token
            token_count += 1
            
            # Send structured data
            data = {
                "token": token,
                "cumulative": cumulative_text,
                "token_count": token_count,
                "done": False
            }
            
            yield f"data: {json.dumps(data)}\n\n"
    
    # Final message with completion metadata
    final_data = {
        "token": "",
        "cumulative": cumulative_text,
        "token_count": token_count,
        "done": True,
        "finish_reason": "complete"
    }
    yield f"data: {json.dumps(final_data)}\n\n"

@app.post("/api/stream-advanced")
async def stream_advanced(query: dict):
    """Streaming with metadata for frontend markdown rendering."""
    prompt = query.get("prompt", "")
    
    return StreamingResponse(
        generate_streaming_with_metadata(prompt),
        media_type="text/event-stream"
    )
```

```javascript
// Frontend: Progressive Markdown Rendering

import MarkdownIt from 'markdown-it';

const md = new MarkdownIt();

async function streamWithMarkdown(prompt) {
    const response = await fetch('/api/stream-advanced', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    let responseElement = document.getElementById('response');
    let buffer = '';
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';  // Keep incomplete line
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                
                // Re-render markdown from cumulative text
                // (More efficient: only render diff, but this is simpler)
                responseElement.innerHTML = md.render(data.cumulative);
                
                // Auto-scroll to bottom
                responseElement.scrollTop = responseElement.scrollHeight;
                
                if (data.done) {
                    console.log(`Complete: ${data.token_count} tokens`);
                    return;
                }
            }
        }
    }
}
```

**Streaming with Cancellation:**

```python
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import uuid

app = FastAPI()

# Track active streams for cancellation
active_streams = {}

async def cancellable_stream(
    prompt: str,
    stream_id: str
) -> AsyncGenerator[str, None]:
    """
    Stream that can be cancelled mid-generation.
    
    Useful when user navigates away or clicks "stop".
    """
    try:
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            # Check for cancellation
            if stream_id not in active_streams:
                print(f"Stream {stream_id} cancelled")
                yield "data: [CANCELLED]\n\n"
                return
            
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                yield f"data: {token}\n\n"
        
        yield "data: [DONE]\n\n"
        
    finally:
        # Clean up
        active_streams.pop(stream_id, None)

@app.post("/api/stream-cancellable")
async def stream_cancellable(query: dict):
    """Start cancellable stream."""
    stream_id = str(uuid.uuid4())
    prompt = query.get("prompt", "")
    
    # Register stream as active
    active_streams[stream_id] = True
    
    # Include stream ID in response header for cancellation
    return StreamingResponse(
        cancellable_stream(prompt, stream_id),
        media_type="text/event-stream",
        headers={"X-Stream-ID": stream_id}
    )

@app.delete("/api/stream/{stream_id}")
async def cancel_stream(stream_id: str):
    """Cancel active stream."""
    if stream_id in active_streams:
        del active_streams[stream_id]
        return {"status": "cancelled", "stream_id": stream_id}
    return {"status": "not_found", "stream_id": stream_id}
```

```javascript
// Frontend: Cancellable streaming

let currentStreamController = null;
let currentStreamId = null;

async function streamWithCancellation(prompt) {
    // Cancel previous stream if exists
    if (currentStreamController) {
        currentStreamController.abort();
    }
    if (currentStreamId) {
        await cancelStream(currentStreamId);
    }
    
    // Start new stream
    currentStreamController = new AbortController();
    
    const response = await fetch('/api/stream-cancellable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
        signal: currentStreamController.signal
    });
    
    currentStreamId = response.headers.get('X-Stream-ID');
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            // Process chunk...
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Stream cancelled by user');
        }
    } finally {
        currentStreamController = null;
        currentStreamId = null;
    }
}

async function cancelStream(streamId) {
    await fetch(`/api/stream/${streamId}`, {
        method: 'DELETE'
    });
}

// Wire up cancel button
document.getElementById('cancelButton').addEventListener('click', () => {
    if (currentStreamController) {
        currentStreamController.abort();
    }
});
```

**Streaming with Error Handling:**

```python
import traceback
import json
from typing import AsyncGenerator

async def stream_with_error_handling(
    prompt: str
) -> AsyncGenerator[str, None]:
    """
    Robust streaming with mid-stream error handling.
    
    Challenges:
    - Can't return HTTP error after stream starts
    - Must signal errors in stream data
    - Need graceful degradation
    """
    try:
        # Yield initial status
        yield f"data: {json.dumps({'type': 'status', 'message': 'Starting generation'})}\n\n"
        
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            timeout=30  # Timeout protection
        )
        
        token_count = 0
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                token_count += 1
                
                # Send token
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        
        # Success completion
        yield f"data: {json.dumps({'type': 'done', 'token_count': token_count})}\n\n"
        
    except TimeoutError:
        # Timeout during streaming
        error_msg = "Generation timed out. Please try again with a shorter prompt."
        yield f"data: {json.dumps({'type': 'error', 'error': error_msg})}\n\n"
        
    except Exception as e:
        # Other errors
        error_msg = f"Error during generation: {str(e)}"
        print(f"Stream error: {traceback.format_exc()}")
        yield f"data: {json.dumps({'type': 'error', 'error': error_msg})}\n\n"

@app.post("/api/stream-robust")
async def stream_robust(query: dict):
    """Streaming endpoint with comprehensive error handling."""
    return StreamingResponse(
        stream_with_error_handling(query.get("prompt", "")),
        media_type="text/event-stream"
    )
```

```javascript
// Frontend: Handle streaming errors

async function robustStream(prompt) {
    const response = await fetch('/api/stream-robust', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    let responseElement = document.getElementById('response');
    responseElement.textContent = '';
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    
                    switch (data.type) {
                        case 'status':
                            console.log(data.message);
                            break;
                            
                        case 'token':
                            responseElement.textContent += data.content;
                            break;
                            
                        case 'done':
                            console.log(`Complete: ${data.token_count} tokens`);
                            return;
                            
                        case 'error':
                            // Display error in UI
                            responseElement.textContent += `\n\n❌ Error: ${data.error}`;
                            console.error(data.error);
                            return;
                    }
                }
            }
        }
    } catch (error) {
        responseElement.textContent += `\n\n❌ Connection error: ${error.message}`;
    }
}
```

### What It Isn't
Streaming responses is not **faster total generation time**. The LLM generates at the same speed whether you stream or buffer. Streaming improves *perceived* latency by showing progress, not actual generation speed.

It's not **always better than buffered responses**. For very short responses (< 50 tokens, < 1 second), streaming overhead may make UX worse. For analytics or batch processing, buffered responses are simpler and sufficient.

Streaming is not **the same as real-time**. While it feels real-time to users, there's still 50-200ms of latency between token generation and client display. True real-time (< 10ms) isn't the goal—responsiveness is.

It's not **simple to implement correctly**. Streaming requires careful handling of async operations, error propagation, cancellation, connection management, and frontend state updates. Non-streaming APIs are much simpler.

Finally, streaming is not **compatible with all deployment patterns**. Some proxies buffer responses, some frontend frameworks don't handle progressive updates well, and some caching strategies break with streaming.

## How It Works

### Production Streaming Patterns

**Pattern 1: Chunked Transfer with Buffering**

```python
import asyncio
from typing import AsyncGenerator

async def stream_with_buffering(
    prompt: str,
    buffer_size: int = 5  # Send every N tokens
) -> AsyncGenerator[str, None]:
    """
    Buffer tokens before sending to reduce HTTP overhead.
    
    Trade-off: Slightly worse perceived latency, fewer HTTP chunks.
    
    Good for: High-volume streaming, reducing server load
    """
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    buffer = []
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            buffer.append(token)
            
            # Send when buffer full
            if len(buffer) >= buffer_size:
                buffered_text = ''.join(buffer)
                yield f"data: {buffered_text}\n\n"
                buffer = []
    
    # Send remaining
    if buffer:
        buffered_text = ''.join(buffer)
        yield f"data: {buffered_text}\n\n"
    
    yield "data: [DONE]\n\n"

# Comparison:
# buffer_size=1: Most responsive, most HTTP overhead (one chunk per token)
# buffer_size=5: Balanced (send every ~5 tokens, ~300ms at 20 tps)
# buffer_size=20: Least overhead, chunkier updates (every ~1 second)
```

**Pattern 2: WebSocket Streaming (Alternative to SSE)**

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """
    WebSocket-based streaming (bidirectional, unlike SSE).
    
    Advantages:
    - Bidirectional (client can send cancel/feedback mid-stream)
    - Better for interactive agents
    - Works through more proxies
    
    Disadvantages:
    - More complex than SSE
    - Requires WebSocket support
    """
    await websocket.accept()
    
    try:
        # Receive prompt from client
        data = await websocket.receive_json()
        prompt = data.get("prompt", "")
        
        # Stream response
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                
                # Send token to client
                await websocket.send_json({
                    "type": "token",
                    "content": token
                })
        
        # Send completion
        await websocket.send_json({
            "type": "done"
        })
        
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        # Send error
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })
    finally:
        await websocket.close()
```

```javascript
// WebSocket client

function streamViaWebSocket(prompt) {
    const ws = new WebSocket('ws://localhost:8000/ws/stream');
    
    ws.onopen = () => {
        // Send prompt
        ws.send(JSON.stringify({ prompt: prompt }));
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
            case 'token':
                document.getElementById('response').textContent += data.content;
                break;
                
            case 'done':
                console.log('Stream complete');
                ws.close();
                break;
                
            case 'error':
                console.error('Error:', data.error);
                ws.close();
                break;
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        console.log('WebSocket closed');
    };
    
    // Return ws for cancellation
    return ws;
}

// Usage with cancellation
let activeWs = streamViaWebSocket("Explain photosynthesis");

// Cancel button
document.getElementById('cancelBtn').addEventListener('click', () => {
    if (activeWs) {
        activeWs.close();
    }
});
```

**Pattern 3: Streaming with Multi-Agent Coordination**

```python
from typing import AsyncGenerator
import json

async def multi_agent_stream(
    user_query: str
) -> AsyncGenerator[str, None]:
    """
    Stream responses from multiple agents in sequence.
    
    Pattern: Research agent → Analysis agent → Response agent
    Each streams its output, with clear transitions.
    """
    # Agent 1: Research
    yield f"data: {json.dumps({'agent': 'researcher', 'status': 'starting'})}\n\n"
    
    research_prompt = f"Research relevant information for: {user_query}"
    research_stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": research_prompt}],
        stream=True
    )
    
    research_text = ""
    for chunk in research_stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            research_text += token
            yield f"data: {json.dumps({'agent': 'researcher', 'token': token})}\n\n"
    
    yield f"data: {json.dumps({'agent': 'researcher', 'status': 'complete'})}\n\n"
    
    # Agent 2: Analysis
    yield f"data: {json.dumps({'agent': 'analyst', 'status': 'starting'})}\n\n"
    
    analysis_prompt = f"Analyze this research and answer: {user_query}\n\nResearch: {research_text}"
    analysis_stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": analysis_prompt}],
        stream=True
    )
    
    for chunk in analysis_stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'agent': 'analyst', 'token': token})}\n\n"
    
    yield f"data: {json.dumps({'agent': 'analyst', 'status': 'complete'})}\n\n"
    yield f"data: {json.dumps({'type': 'done'})}\n\n"

@app.post("/api/stream-multi-agent")
async def stream_multi_agent(query: dict):
    """Multi-agent streaming endpoint."""
    return StreamingResponse(
        multi_agent_stream(query.get("query", "")),
        media_type="text/event-stream"
    )
```

## Think of It Like This
Imagine you're watching a chef prepare a meal through a restaurant's open kitchen window.

**Non-streaming** is like the chef preparing the entire meal behind closed doors, then suddenly presenting it all at once. You wait 20 minutes with no updates, wondering: Did they forget my order? Is something wrong? How much longer? When the meal finally arrives, you're relieved but frustrated by the uncertainty.

**Streaming** is like watching the chef work: chopping vegetables (first tokens arriving), sautéing ingredients (continuous progress), plating the dish (nearing completion). The total preparation time is the same 20 minutes, but you're engaged, seeing progress, and confident your meal is being prepared. If you see them add an ingredient you're allergic to, you can stop them immediately (early cancellation) rather than discovering it when the finished dish arrives.

Streaming responses give users that "open kitchen" experience—they see the AI working, understand progress, and can intervene if needed. The work takes the same time, but the experience transforms from anxious waiting to engaged observation.

## The "So What?" Factor
**If you implement streaming responses:**
- Users perceive system as 5-10x more responsive despite similar total time
- Can display first tokens in 200-500ms (feels instant)
- Users tolerate 20+ second responses (reading while generating)
- Early cancellation saves 50-70% of completion costs
- Users can detect off-topic responses and stop them
- Enables reading while generation continues (parallel processing)
- Improved perceived performance metrics (time-to-first-token < 1s)
- Better user engagement (watching progress vs waiting blindly)
- Reduced perceived "system crashed" complaints
- Competitive UX with modern AI applications

**If you don't implement streaming:**
- Users abandon after 5-8 seconds of silence (too slow)
- No way to show progress or system status
- Users can't cancel—must wait for completion even if wrong
- Pay for full completion even when users don't need it
- Perceived latency 5-10x worse despite similar actual time
- Users complain system is "broken" or "hanging"
- Can't compete with streaming-enabled competitors
- Higher bounce rates and user frustration
- More support tickets ("Is it working?")
- Outdated UX by 2026 standards

## Practical Checklist
Before deploying streaming responses:
- [ ] Have you chosen appropriate protocol (SSE vs WebSocket)?
- [ ] Is streaming enabled on LLM API calls (`stream=True`)?
- [ ] Does backend use async generators for efficient streaming?
- [ ] Are SSE headers configured correctly (no-cache, keep-alive)?
- [ ] Does frontend handle partial updates without re-rendering entire page?
- [ ] Is there error handling for mid-stream failures?
- [ ] Can users cancel streaming mid-generation?
- [ ] Are streaming connections cleaned up on disconnect?
- [ ] Does streaming work through your CDN/proxy? (Some buffer responses)
- [ ] Is there fallback for browsers without SSE support?
- [ ] Are you buffering tokens for performance? (Reduce HTTP overhead)
- [ ] Is markdown/rich text rendered progressively without flickering?
- [ ] Have you tested streaming with slow connections?

## Watch Out For
⚠️ **Proxy/CDN Buffering**: Many proxies (nginx, CloudFlare) buffer responses by default. This defeats streaming—tokens arrive in large chunks. Must configure: `X-Accel-Buffering: no` (nginx), disable response buffering (CloudFlare).

⚠️ **Connection Timeout Issues**: SSE connections stay open for 10-30 seconds. Some load balancers or proxies timeout idle connections. Configure timeouts > expected generation time.

⚠️ **Memory Leaks from Unclosed Streams**: If client disconnects mid-stream but server doesn't detect it, generator keeps running, consuming resources. Implement disconnect detection and cleanup.

⚠️ **Progressive Markdown Rendering Flickering**: Re-rendering entire markdown on each token causes visual flicker. Solution: render less frequently (every 5-10 tokens) or use differential rendering.

⚠️ **CORS Issues with SSE**: SSE requests must respect CORS. If your frontend is on different domain than backend, configure CORS headers correctly.

⚠️ **No Retry on Connection Failure**: SSE doesn't auto-reconnect. If connection drops mid-stream, client must detect and re-request from beginning or implement resumption.

⚠️ **Streaming + Caching Conflicts**: Caching streaming responses is complex. Can cache after completion, but can't cache partial streams. Strategy: buffer complete response server-side, cache it, then stream to client.

⚠️ **Token Buffering Trade-offs**: Buffering tokens (send every N tokens) reduces HTTP overhead but increases perceived latency. Balance based on token generation speed and network conditions.

⚠️ **Error Handling Complexity**: Once stream starts, can't return HTTP error codes. Must signal errors in-stream using structured messages. Frontend must handle mid-stream errors gracefully.

⚠️ **Mobile Browser SSE Support**: Some mobile browsers have limited SSE support or aggressive connection closing. Test thoroughly or use WebSocket fallback.

## Connections
**Builds On:**
- Async programming patterns
- HTTP protocols (SSE, WebSocket)
- LLM APIs and token generation
- Event-driven architectures

**Works With:**
- [context_window](../Data_and_Retrieval_Patterns/context_window.md) - Streaming helps when responses approach context limits
- [caching](../Data_and_Retrieval_Patterns/caching.md) - Must buffer complete response before caching
- [handoff_protocol](handoff_protocol.md) - Stream handoff context progressively
- Frontend frameworks (React, Vue, Svelte)
- WebSocket infrastructure

**Leads To:**
- Progressive enhancement patterns
- Real-time collaborative agents
- Multi-modal streaming (text + images + code)
- Streaming with tool use (stream tool calls as they happen)
- Adaptive streaming (adjust buffer size based on network)

**Related Patterns:**
- [error_handling](error_handling.md) - Mid-stream error propagation
- Server-Sent Events (SSE) specification
- WebSocket protocol
- Async/await patterns
- Generator functions and iterators

## Quick Decision Guide
**Use streaming when:**
- Responses typically > 100 tokens (> 2 seconds)
- User-facing interactive applications
- Users benefit from reading while generating
- Want to enable early cancellation
- Need to show progress for long generations
- Building chat interfaces or conversational UI
- Competing with other AI applications (UX expectation)

**Use buffered responses when:**
- Responses typically < 50 tokens (< 1 second)
- Batch processing or background jobs
- API-to-API communication (no human watching)
- Need response caching (simpler with complete responses)
- Simple infrastructure requirements preferred
- Analytics or logging use cases

**Use WebSocket instead of SSE when:**
- Need bidirectional communication (client sends feedback mid-stream)
- Building interactive/collaborative agents
- Proxies aggressively buffer HTTP responses
- Want more control over connection lifecycle

**Buffer tokens (send every N) when:**
- High server load (reduce HTTP overhead)
- Network latency high (batch reduces round-trips)
- Token generation very fast (60+ tokens/sec)

**Send every token when:**
- Lowest possible perceived latency critical
- Token generation slower (15-30 tokens/sec)
- Server load manageable
- Network latency low

## Further Exploration
- 📖 **Server-Sent Events (SSE) Specification** - W3C standard for HTTP streaming
- 🎯 **OpenAI Streaming API Documentation** - Reference implementation of LLM streaming
- 💡 **Implement Streaming + Cancellation** - Build chat UI with token-by-token display and cancel button
- 📖 **"High Performance Browser Networking"** - Grigorik (Chapter on SSE vs WebSocket)
- 🎯 **FastAPI Streaming Response Patterns** - Production-grade async streaming examples
- 💡 **Test Streaming Through Proxies** - Configure nginx/CloudFlare to allow SSE passthrough
- 📖 **React/Vue Streaming Integration** - Patterns for progressive UI updates without flicker
- 🎯 **Vercel AI SDK Streaming** - Study modern streaming abstractions for Next.js
- 💡 **Measure Perceived vs Actual Latency** - A/B test streaming vs buffered, measure user preference
- 📖 **WebSocket Protocol RFC 6455** - Deep dive into WebSocket for advanced use cases

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*

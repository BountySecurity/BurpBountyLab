"""AI / LLM-related disclosure endpoints.

Each route here is designed to trigger one or more Burp Bounty profiles shipped
alongside this project:

- AI-Specific-Header-Disclosure        (x-ai-backend / x-rag-provider / x-llm-provider /
                                        x-openai-model / x-anthropic-model / x-embedding-model /
                                        x-mcp-enabled / x-model: gpt|claude|...)
- Gateway-Fingerprinting               (x-kong-* / x-envoy-* response headers)
- Health-Status-Endpoint-Discovery     (URL path filenames: health, healthz, status,
                                        ready, readyz, live, liveness, metrics)
- Health-Status-Metadata-Exposure      (JSON/text with rag_enabled, mcp_enabled,
                                        embedding_model, vector_db, *_tokens,
                                        model_name/model_provider/llm_provider,
                                        service_version)
- OpenAI-Compatible-API-Fingerprinting (JSON with prompt_tokens/completion_tokens/
                                        total_tokens + choices + model, or chatcmpl-*)
- RateLimit-Headers-Disclosure         (RateLimit-* and X-RateLimit-* headers)
"""

from flask import Blueprint, jsonify, make_response, request

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


# ---------------------------------------------------------------------------
# Header helpers
# ---------------------------------------------------------------------------
def _ai_headers(resp, model='gpt-4o-mini', provider='openai',
                anthropic_model='claude-3-5-sonnet-20241022',
                embedding_model='text-embedding-3-small',
                rag_provider='pinecone', mcp_enabled='true'):
    """Adds the headers picked up by AI-Specific-Header-Disclosure."""
    resp.headers['X-AI-Backend'] = f'vllm-0.6.3 ({provider})'
    resp.headers['X-RAG-Provider'] = rag_provider
    resp.headers['X-LLM-Provider'] = provider
    resp.headers['X-OpenAI-Model'] = model
    resp.headers['X-Anthropic-Model'] = anthropic_model
    resp.headers['X-Embedding-Model'] = embedding_model
    resp.headers['X-MCP-Enabled'] = mcp_enabled
    resp.headers['X-Model'] = model  # matches gpt|claude|gemini|llama|mistral|...
    return resp


def _gateway_headers(resp):
    """Adds the headers picked up by Gateway-Fingerprinting."""
    resp.headers['X-Kong-Upstream-Latency'] = '12'
    resp.headers['X-Kong-Proxy-Latency'] = '3'
    resp.headers['X-Kong-Request-Id'] = 'a1b2c3d4e5f6'
    resp.headers['X-Envoy-Upstream-Service-Time'] = '42'
    resp.headers['X-Envoy-Decorator-Operation'] = 'llm-gateway.ai.svc.cluster.local:8080/*'
    resp.headers['X-Envoy-Attempt-Count'] = '1'
    return resp


def _ratelimit_headers(resp):
    """Adds the headers picked up by RateLimit-Headers-Disclosure."""
    resp.headers['RateLimit-Limit'] = '60'
    resp.headers['RateLimit-Remaining'] = '57'
    resp.headers['RateLimit-Reset'] = '42'
    resp.headers['X-RateLimit-Limit'] = '60'
    resp.headers['X-RateLimit-Remaining'] = '57'
    resp.headers['X-RateLimit-Reset'] = '1747300000'
    return resp


def _decorate(resp):
    """Apply AI + gateway + rate-limit headers in one shot."""
    _ai_headers(resp)
    _gateway_headers(resp)
    _ratelimit_headers(resp)
    return resp


# ---------------------------------------------------------------------------
# OpenAI-compatible API surface
# ---------------------------------------------------------------------------
@ai_bp.route('/v1/chat/completions', methods=['GET', 'POST'])
def chat_completions():
    """Triggers: OpenAI-Compatible-API-Fingerprinting (choices + model +
    *_tokens + chatcmpl-* id), AI-Specific-Header-Disclosure,
    Gateway-Fingerprinting, RateLimit-Headers-Disclosure."""
    body = {
        "id": "chatcmpl-9xK2pQrStUvWxYzAbCdEfGhIjKl",
        "object": "chat.completion",
        "created": 1747300000,
        "model": "gpt-4o-mini",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello from the vulnerable AI lab."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 24,
            "completion_tokens": 11,
            "total_tokens": 35
        }
    }
    resp = make_response(jsonify(body))
    return _decorate(resp)


@ai_bp.route('/v1/completions', methods=['GET', 'POST'])
def text_completions():
    """Triggers: OpenAI-Compatible-API-Fingerprinting + AI headers + gateway +
    rate-limit."""
    body = {
        "id": "chatcmpl-legacyZ9Y8X7W6V5U4T3S2R1Q0",
        "object": "text_completion",
        "created": 1747300000,
        "model": "gpt-3.5-turbo-instruct",
        "choices": [
            {
                "text": "vulnerable response",
                "index": 0,
                "finish_reason": "length"
            }
        ],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 4,
            "total_tokens": 13
        }
    }
    resp = make_response(jsonify(body))
    return _decorate(resp)


@ai_bp.route('/v1/embeddings', methods=['GET', 'POST'])
def embeddings():
    """Triggers: AI-Specific-Header-Disclosure, Gateway-Fingerprinting,
    RateLimit-Headers-Disclosure, Health-Status-Metadata-Exposure (embedding_model,
    model_provider, total_tokens)."""
    body = {
        "object": "list",
        "data": [
            {"object": "embedding", "index": 0, "embedding": [0.01, -0.02, 0.03]}
        ],
        "model": "text-embedding-3-small",
        "model_provider": "openai",
        "embedding_model": "text-embedding-3-small",
        "usage": {
            "prompt_tokens": 7,
            "total_tokens": 7
        }
    }
    resp = make_response(jsonify(body))
    return _decorate(resp)


@ai_bp.route('/v1/models')
def models_list():
    """Triggers: AI-Specific-Header-Disclosure, Health-Status-Metadata-Exposure
    (model_name, model_provider, llm_provider)."""
    body = {
        "object": "list",
        "data": [
            {"id": "gpt-4o-mini", "object": "model", "model_name": "gpt-4o-mini",
             "model_provider": "openai", "llm_provider": "openai"},
            {"id": "claude-3-5-sonnet-20241022", "object": "model",
             "model_name": "claude-3-5-sonnet-20241022",
             "model_provider": "anthropic", "llm_provider": "anthropic"},
            {"id": "llama-3.1-70b-instruct", "object": "model",
             "model_name": "llama-3.1-70b-instruct",
             "model_provider": "meta", "llm_provider": "vllm"}
        ]
    }
    resp = make_response(jsonify(body))
    return _decorate(resp)


# ---------------------------------------------------------------------------
# Health / status / metrics surface (Health-Status-Endpoint-Discovery filenames)
# ---------------------------------------------------------------------------
def _metadata_payload():
    """Common AI-flavoured metadata payload that triggers
    Health-Status-Metadata-Exposure."""
    return {
        "status": "ok",
        "service_version": "1.4.2-rag",
        "model_name": "gpt-4o-mini",
        "model_provider": "openai",
        "llm_provider": "openai",
        "embedding_model": "text-embedding-3-small",
        "vector_db": "pinecone",
        "rag_enabled": True,
        "mcp_enabled": True,
        "usage": {
            "prompt_tokens": 12345,
            "completion_tokens": 6789,
            "total_tokens": 19134
        }
    }


@ai_bp.route('/health')
def health():
    """Triggers: Health-Status-Endpoint-Discovery (health),
    Health-Status-Metadata-Exposure, plus AI / gateway / rate-limit headers."""
    resp = make_response(jsonify(_metadata_payload()))
    return _decorate(resp)


@ai_bp.route('/healthz')
def healthz():
    """Triggers: Health-Status-Endpoint-Discovery (healthz) +
    Health-Status-Metadata-Exposure."""
    resp = make_response(jsonify(_metadata_payload()))
    return _decorate(resp)


@ai_bp.route('/status')
def status():
    """Triggers: Health-Status-Endpoint-Discovery (status) +
    Health-Status-Metadata-Exposure."""
    resp = make_response(jsonify(_metadata_payload()))
    return _decorate(resp)


@ai_bp.route('/ready')
def ready():
    """Triggers: Health-Status-Endpoint-Discovery (ready) +
    Health-Status-Metadata-Exposure."""
    resp = make_response(jsonify({
        "ready": True,
        "rag_enabled": True,
        "vector_db": "weaviate",
        "embedding_model": "bge-large-en-v1.5",
        "service_version": "1.4.2-rag"
    }))
    return _decorate(resp)


@ai_bp.route('/readyz')
def readyz():
    """Triggers: Health-Status-Endpoint-Discovery (readyz) +
    Health-Status-Metadata-Exposure."""
    resp = make_response(jsonify({
        "ready": True,
        "mcp_enabled": True,
        "model_provider": "anthropic",
        "model_name": "claude-3-5-sonnet-20241022",
        "service_version": "1.4.2-rag"
    }))
    return _decorate(resp)


@ai_bp.route('/live')
def live():
    """Triggers: Health-Status-Endpoint-Discovery (live) +
    Health-Status-Metadata-Exposure (text/plain)."""
    body = (
        "live=true\n"
        "service_version=1.4.2-rag\n"
        "model_name=gpt-4o-mini\n"
        "model_provider=openai\n"
        "embedding_model=text-embedding-3-small\n"
        "rag_enabled=true\n"
        "mcp_enabled=true\n"
    )
    resp = make_response(body, 200)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return _decorate(resp)


@ai_bp.route('/liveness')
def liveness():
    """Triggers: Health-Status-Endpoint-Discovery (liveness) +
    Health-Status-Metadata-Exposure."""
    resp = make_response(jsonify({
        "live": True,
        "llm_provider": "openai",
        "model_name": "gpt-4o-mini",
        "service_version": "1.4.2-rag",
        "rag_enabled": True
    }))
    return _decorate(resp)


@ai_bp.route('/metrics')
def metrics():
    """Triggers: Health-Status-Endpoint-Discovery (metrics) +
    Health-Status-Metadata-Exposure (text/plain prometheus-style)."""
    body = (
        "# HELP prompt_tokens Number of prompt tokens served.\n"
        "# TYPE prompt_tokens counter\n"
        "prompt_tokens{model_name=\"gpt-4o-mini\",model_provider=\"openai\"} 12345\n"
        "# HELP completion_tokens Number of completion tokens served.\n"
        "# TYPE completion_tokens counter\n"
        "completion_tokens{model_name=\"gpt-4o-mini\",model_provider=\"openai\"} 6789\n"
        "# HELP total_tokens Total tokens served.\n"
        "# TYPE total_tokens counter\n"
        "total_tokens{llm_provider=\"openai\",embedding_model=\"text-embedding-3-small\"} 19134\n"
        "# HELP service_info Static service metadata.\n"
        "# TYPE service_info gauge\n"
        "service_info{service_version=\"1.4.2-rag\",vector_db=\"pinecone\","
        "rag_enabled=\"true\",mcp_enabled=\"true\"} 1\n"
    )
    resp = make_response(body, 200)
    resp.headers['Content-Type'] = 'text/plain; version=0.0.4; charset=utf-8'
    return _decorate(resp)


# ---------------------------------------------------------------------------
# Dedicated focused triggers (handy for isolating profiles during testing)
# ---------------------------------------------------------------------------
@ai_bp.route('/headers')
def ai_headers_only():
    """Triggers: AI-Specific-Header-Disclosure (only AI headers, no body markers)."""
    resp = make_response('<html><body><h1>AI headers demo</h1></body></html>')
    return _ai_headers(resp)


@ai_bp.route('/gateway')
def gateway_only():
    """Triggers: Gateway-Fingerprinting (Kong + Envoy headers)."""
    resp = make_response('<html><body><h1>Behind Kong + Envoy</h1></body></html>')
    return _gateway_headers(resp)


@ai_bp.route('/ratelimit')
def ratelimit_only():
    """Triggers: RateLimit-Headers-Disclosure (RateLimit-* and X-RateLimit-* headers)."""
    resp = make_response('<html><body><h1>Rate-limited endpoint</h1></body></html>')
    return _ratelimit_headers(resp)


@ai_bp.route('/mcp/tools')
def mcp_tools():
    """Triggers: AI-Specific-Header-Disclosure (x-mcp-enabled, x-model) +
    Health-Status-Metadata-Exposure (mcp_enabled, model_provider, service_version)."""
    body = {
        "mcp_enabled": True,
        "model_provider": "anthropic",
        "model_name": "claude-3-5-sonnet-20241022",
        "service_version": "1.4.2-rag",
        "tools": [
            {"name": "search", "description": "Search the knowledge base"},
            {"name": "fetch_url", "description": "Fetch a remote URL"}
        ]
    }
    resp = make_response(jsonify(body))
    return _decorate(resp)

import json
import os
import logging
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from tenacity import retry, wait_fixed, stop_after_attempt, after_log
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
from .routers import chat, auth
from .services.nlu_service import NLU_Service
from .services.response_engine_service import ResponseEngineService
from .utils.auth import verify_access_token

# Setup structured logging
LOG_FORMAT = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "service": "backend"}'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Setup OpenTelemetry Jaeger
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)
tracer = trace.get_tracer(__name__)

# FastAPI app
app = FastAPI()

# Add Prometheus instrumentator
Instrumentator().instrument(app).expose(app)

# CORS middleware - In production, you should specify your frontend domain
origins = ["http://localhost:8080", "https://your-frontend-domain.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT auth dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)

# Initialize services
nlu_service = NLU_Service()
response_engine_service = ResponseEngineService()
redis_client: aioredis.Redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))

app.include_router(chat.router)
app.include_router(auth.router, prefix="/api/auth")

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Service is healthy"}

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "guest"):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    logger.info(f"User {user_id} connected via WebSocket.")
    try:
        while True:
            user_message = await websocket.receive_text()
            
            # Use OpenTelemetry to trace the request flow
            with tracer.start_as_current_span("process_user_message") as span:
                span.set_attribute("user.id", user_id)
                span.set_attribute("message.text", user_message)

                # 1. Call NLU Service with Redis cache
                nlu_result = await nlu_service.parse_with_cache(user_message, redis_client)
                
                # 2. Call Response Engine Service with retry
                bot_response = await response_engine_service.generate_response(
                    intent=nlu_result.get("intent", {}).get("name"),
                    slots=nlu_result.get("entities", {})
                )
                
                # 3. Send response back
                await websocket.send_json({"user_id": "bot", "text": bot_response})
                logger.info(f"Bot responded to {user_id} with: {bot_response}")

    except WebSocketDisconnect:
        logger.info(f"User {user_id} disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({"user_id": "bot", "text": "服務異常，請稍後再試。"})

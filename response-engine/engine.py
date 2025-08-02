import os
import openai
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Dict, Any
from tenacity import retry, wait_fixed, stop_after_attempt, after_log
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup structured logging
LOG_FORMAT = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "service": "response-engine"}'
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

app = FastAPI()

class GenerateRequest(BaseModel):
    intent: str
    slots: Dict[str, Any]

@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "message": "Service is healthy"}

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3), after=after_log(logger, logging.WARNING))
@app.post("/generate")
async def generate_response(request: GenerateRequest) -> Dict[str, str]:
    """
    根據意圖和槽位，使用 GPT-3.5 產生自然回應。
    """
    with tracer.start_as_current_span("generate_response_from_openai") as span:
        span.set_attribute("intent.name", request.intent)
        span.set_attribute("slots.data", str(request.slots))
        
        prompt_template = "根據意圖 {intent} 和資訊 {slots}，以口語化方式生成一個簡短的回應。"
        formatted_prompt = prompt_template.format(intent=request.intent, slots=request.slots)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=formatted_prompt,
                max_tokens=100,
                temperature=0.7
            )
            generated_text = response.choices[0].text.strip()
            span.set_attribute("generated.response", generated_text)
            return {"response": generated_text}
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            raise e

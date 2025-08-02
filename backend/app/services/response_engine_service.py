import aiohttp
import os
from typing import Dict, Any
from tenacity import retry, wait_fixed, stop_after_attempt, after_log
import logging

logger = logging.getLogger(__name__)

class ResponseEngineService:
    def __init__(self, engine_url: str = os.getenv("RESPONSE_ENGINE_URL", "http://response-engine:8001")):
        self.engine_url = engine_url

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3), after=after_log(logger, logging.WARNING))
    async def generate_response(self, intent: str, slots: Dict[str, Any]) -> str:
        """
        將 NLU 結果發送給 Response Engine 服務產生回應。
        """
        payload = {"intent": intent, "slots": slots}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.engine_url}/generate", json=payload, timeout=10) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get("response", "很抱歉，我現在無法生成回應。")

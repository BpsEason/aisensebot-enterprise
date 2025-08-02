import aiohttp
import os
import json
from typing import Dict, Any
from redis.asyncio import Redis

class NLU_Service:
    def __init__(self, nlu_url: str = os.getenv("RASA_URL", "http://nlu:5005")):
        self.nlu_url = nlu_url

    async def parse_message(self, text: str) -> Dict[str, Any]:
        """
        將訊息發送給 Rasa NLU 服務進行解析。
        """
        payload = {"text": text}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.nlu_url}/model/parse", json=payload, timeout=5) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Error calling NLU service: {e}")
                return {"intent": {"name": "default"}, "entities": {}}
    
    async def parse_with_cache(self, text: str, redis_client: Redis) -> Dict[str, Any]:
        """
        先從 Redis 快取查詢，若無則呼叫 NLU 服務並存入快取。
        """
        cache_key = f"nlu:{text}"
        cached_result = await redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)

        nlu_result = await self.parse_message(text)
        await redis_client.set(cache_key, json.dumps(nlu_result), ex=3600) # 快取一小時
        
        return nlu_result

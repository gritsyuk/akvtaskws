import aioredis
import json
from typing import Optional
from settings import logfire


class RedisClient:
    def __init__(self, redis_url: str = "redis://redis:6379"):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        if not self.redis:
            self.redis = await aioredis.from_url(
                self.redis_url, encoding="utf-8", decode_responses=True
            )
            logfire.info("Подключение к Redis установлено")

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None
            logfire.info("Соединение с Redis закрыто")

    async def save_event(self, event_data: dict):
        try:
            await self.connect()
            event_id = f"event:{event_data.get('id', 'unknown')}"
            await self.redis.set(event_id, json.dumps(event_data, ensure_ascii=False))
            logfire.info(f"Событие сохранено в Redis: {event_id}")
        except Exception as e:
            logfire.error(f"Ошибка при сохранении в Redis: {e}")
        finally:
            await self.close()

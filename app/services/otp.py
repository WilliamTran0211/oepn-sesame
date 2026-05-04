import secrets

from app.common.enum import VerificationPurpose
from app.core.redis import RedisClient


class OTPService:
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client
        self.ttl = 300

    async def generate(self, user_id: str, purpose: VerificationPurpose) -> str:
        otp = f"{secrets.randbelow(1000000):06d}"
        key = f"otp:{purpose}:{user_id}"
        await self.redis.setex(key, self.ttl, otp)

        return otp

    async def verify(self, user_id: str, purpose: str, otp: str) -> bool:
        key = f"otp:{purpose}:{user_id}"
        saved = await self.redis.get(key)

        if saved and saved == otp:
            await self.redis.delete(key)
            return True
        return False

    async def is_rate_limited(self, user_id: str, purpose: str, limit: int = 3) -> bool:
        key = f"otp:rate:{purpose}:{user_id}"
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, 3600)

        return count > limit

import json

from redis import Redis

from src.config import Config


config = Config()


class Cacher:
    def __init__(self, key_prefix: str):
        self.client = Redis.from_url(config.REDIS_URL)
        self.key_prefix = key_prefix

    def __get_key(self, key: str) -> str:
        return f"{self.key_prefix}:{key}"

    def get(self, key: str):
        key = self.__get_key(key)
        result = self.client.get(key)
        
        if result:
            try:
                return json.loads(result)
            except (json.JSONDecodeError, TypeError):
                return result

        return result

    def set(self, key: str, value: str | dict | None, ttl: int = None) -> bool:
        key = self.__get_key(key)
        result = None

        if isinstance(value, dict):
            value = json.dumps(value)

        if ttl:
            result = self.client.set(key, value, ex=ttl)
        else:
            result = self.client.set(key, value)

        return result

    def delete(self, key: str) -> bool:
        key = self.__get_key(key)
        return self.client.delete(key)

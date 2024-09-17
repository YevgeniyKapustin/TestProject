from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn
from fastapi import FastAPI

from comments.router import router as comment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield

app = FastAPI(
    title='Комментарии',
    version='1.0',
    lifespan=lifespan,
    swagger_ui_parameters={
        'operationsSorter': 'method',
        'defaultModelsExpandDepth': -1
    },
)
app.include_router(comment_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

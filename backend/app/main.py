# uvicorn app.main:app --reload --port=8000

from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

import torch

@asynccontextmanager
async def lifespan(app: FastAPI):
    if torch.backends.mps.is_available():
        print("MPS를 사용합니다.")
        device = "mps"
    elif torch.cuda.is_available():
        print("CUDA를 사용합니다.")
        device = "cuda"
    else:
        print("CUDA나 MPS를 찾을 수 없습니다. CPU를 사용합니다.")
        device = "cpu"

    app.state.semaphore = asyncio.Semaphore(1)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root_page():
    return "hello"
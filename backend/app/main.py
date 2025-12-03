# uvicorn app.main:app --reload --port=8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import time

import torch
from diffusers import ZImagePipeline

from app.core.logger import logger
from app.core.middleware import setup_cors
from app.api.v1.endpoints.generate.generate import router as generate_rounter

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작시 1번만 Diffusers Pipeline 초기화"""

    # device 감지
    if torch.backends.mps.is_available():
        logger.info("MPS를 사용합니다.")
        device = "mps"
    elif torch.cuda.is_available():
        logger.info("CUDA를 사용합니다.")
        device = "cuda"
    else:
        logger.info("CUDA나 MPS를 찾을 수 없습니다. CPU를 사용합니다.")
        device = "cpu"

    # Pipeline 정의
    logger.info("ZImagePipeline 로딩 시작...")
    t0 = time.perf_counter()

    pipe = ZImagePipeline.from_pretrained(
        "../model/Z-Image-Turbo", # /model 폴더에 있는 Z Image Turbo 사용
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=False,
    )

    # 감지한 device 사용
    pipe.to(device)
    pipe.enable_attention_slicing()

    load_time = time.perf_counter() - t0
    logger.info(f"ZImagePipeline 로딩 완료 ({load_time:.2f}초 소요)")

    app.state.pipe = pipe
    app.state.device = device
    app.state.semaphore = asyncio.Semaphore(1) # 동시 생성 1개로 제한

    try:
        yield
    finally:
        del app.state.pipe

app = FastAPI(lifespan=lifespan)

setup_cors(app)

app.include_router(generate_rounter)

@app.get("/ping")
async def ping():
    return "pong"
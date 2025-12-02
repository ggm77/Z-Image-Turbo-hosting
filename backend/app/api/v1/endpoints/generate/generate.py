from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
import asyncio
from io import BytesIO

from diffusers import ZImagePipeline

from app.schemas.generate.generate import GenerateRequest
from app.utils.pipeline_runner import run_pipeline_async

router = APIRouter(
    prefix="/api/v1",
    tags=["generate"],
)

def get_pipe(request: Request) -> ZImagePipeline:
    return request.app.state.pipe

def get_device(request: Request) -> str:
    return request.app.state.device

def get_semaphore(request: Request) -> asyncio.Semaphore:
    return request.app.state.semaphore

@router.post("/generate")
async def generate(
    body: GenerateRequest,
    pipe: ZImagePipeline = Depends(get_pipe),
    device: str = Depends(get_device),
    semaphore: asyncio.Semaphore = Depends(get_semaphore),
):
    async with semaphore:
        buf: BytesIO = await run_pipeline_async(pipe, device, body)

    return StreamingResponse(buf, media_type="image/png")
from io import BytesIO
import time

import anyio
import torch
from diffusers import ZImagePipeline

from app.core.logger import logger
from app.schemas.generate.generate import GenerateRequest

async def run_pipeline_async(
        pipe: ZImagePipeline,
        device: str,
        data: GenerateRequest
) -> BytesIO:
    """
    Diffusers pipeline 호출은 blocking이므로
    anyio.to_thread.run_sync로 스레드풀에서 실행
    """

    def _sync_call() -> BytesIO:
        
        generator = torch.Generator(device=device).manual_seed(data.seed)
        start_time = time.perf_counter()

        def on_step_end(pipeline, step_index, timestep, callback_kwargs):
            total = pipeline.num_timesteps
            progress = (step_index + 1) / total * 100
            
            """ progress를 웹 소켓으로 뿌려서 프론트가 알게 하기 """

            logger.info(f"[ZImage] step {step_index+1}/{total} ({progress:.1f}%)")

            return callback_kwargs



        out = pipe(
            prompt=data.prompt,
            height=data.height,
            width=data.width,
            num_inference_steps=data.num_inference_steps,
            guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
            generator=generator,
            callback_on_step_end=on_step_end,
        )

        image = out.images[0]
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)

        elapsed_time = time.perf_counter() - start_time
        logger.info(f"[ZImage] 이미지 생성 완료 ({elapsed_time:.2f}초 소요)")

        return buf
    
    return await anyio.to_thread.run_sync(_sync_call)
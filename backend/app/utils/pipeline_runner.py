from io import BytesIO

import anyio
import torch

from app.schemas.generate.generate import GenerateRequest

async def run_pipeline_async(
        pipe: str,
        device: str,
        data: GenerateRequest
) -> BytesIO:
    """
    Diffusers pipeline 호출은 blocking이므로
    anyio.to_thread.run_sync로 스레드풀에서 실행
    """

    def _sync_call() -> BytesIO:
        
        generator = torch.Generator(device=device).manual_seed(data.seed)

        out = pipe(
            prompt=data.prompt,
            height=data.height,
            width=data.width,
            num_inference_steps=data.num_inference_steps,
            guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
            generator=generator,
        )

        image = out.images[0]
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf
    
    return await anyio.to_thread.run_sync(_sync_call)
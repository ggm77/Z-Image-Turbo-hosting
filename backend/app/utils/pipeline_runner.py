import time
from datetime import datetime

import torch
from diffusers import ZImagePipeline

from app.core.logger import logger

from app.db.session import get_db_connection
from app.core.config import settings

# 이미지 생성하는 함수
def run_pipeline(
        task_id: str,
        prompt: str,
        height: int,
        width: int,
        num_inference_steps: int,
        seed: int,
        pipe: ZImagePipeline,
        device: str,
        semaphore
):
    # 전역 세마포어로 동시 생성 제한
    with semaphore:

        # DB 연결
        with get_db_connection() as conn:

            try:
                # 상태를 processing으로 변경
                conn.execute(
                    "UPDATE tasks SET status = ? WHERE task_id = ?",
                    ("processing", task_id)
                )
                conn.commit()
            
                # 이미지 생성 준비
                generator = torch.Generator(device=device).manual_seed(seed)
                start_time = time.perf_counter()

                # 이미지 생성 콜백 함수
                def on_step_end(pipeline, step_index, timestep, callback_kwargs):
                    total = pipeline.num_timesteps
                    progress = (step_index + 1) / total * 100
                    
                    """ progress를 웹 소켓으로 뿌려서 프론트가 알게 하기 """

                    logger.info(f"[ZImage] step {step_index+1}/{total} ({progress:.1f}%)")

                    return callback_kwargs

                # 이미지 생성 실행
                out = pipe(
                    prompt=prompt,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=0.0,     # Guidance should be 0 for the Turbo models
                    generator=generator,
                    callback_on_step_end=on_step_end,
                )

                # 이미지 저장
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                image = out.images[0]
                file_name = f"{current_time}_{task_id}.png"
                file_path = settings.IMG_DIR + "/" + file_name
                image.save(file_path, format="PNG")

                # 상태를 completed로 변경
                conn.execute(
                    "UPDATE tasks SET status = ?, file_path = ? WHERE task_id = ?",
                    ("completed", file_name, task_id)
                )
                conn.commit()

                # 로깅
                elapsed_time = time.perf_counter() - start_time
                logger.info(f"[ZImage] 이미지 생성 완료 ({elapsed_time:.2f}초 소요)")
        
            except Exception as ex:
                logger.error(f"[ZImage] 이미지 생성 중 오류 발생: {ex}")
                conn.execute(
                    "UPDATE tasks SET status = ? WHERE task_id = ?",
                    ("failed", task_id)
                )
                conn.commit()
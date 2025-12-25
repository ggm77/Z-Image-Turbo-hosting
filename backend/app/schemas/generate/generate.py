from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    height: int = 512
    width: int = 512
    num_inference_steps: int = 9
    seed: int = 42

class GenerateResponse(BaseModel):
    task_id: str
    status: str
    prompt: str
    height: int
    width: int
    num_inference_steps: int
    seed: int
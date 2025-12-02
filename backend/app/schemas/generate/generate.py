from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    height: int = 512
    width: int = 512
    num_inference_steps: int = 9
    seed: int = 42
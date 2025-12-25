from pydantic import BaseModel

class TasksResponse(BaseModel):
    task_id: str
    status: str
    created_at: str
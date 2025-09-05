from pydantic import BaseModel, Field
class Subject(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Matematicas"])

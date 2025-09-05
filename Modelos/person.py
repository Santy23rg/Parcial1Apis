from pydantic import BaseModel, Field
class Person(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Santiago Roldan"])
    email: str = Field(..., examples=["Santiago.Roldan@gmail.com"])
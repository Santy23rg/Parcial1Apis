from pydantic import BaseModel, Field
class Note(BaseModel):
    estudiante: int = Field(..., examples=[1])
    profesor: int = Field(..., examples=[1])
    materia: int = Field(..., examples=[1])
    nota: float = Field(..., examples=[1.1])
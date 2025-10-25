from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_services import chat

router = APIRouter()

class LLMQuery(BaseModel):
    question: str

@router.post("/chat")
def ask_llm(query: LLMQuery):
    response = chat(query.question)
    return {"response": response}

from fastapi import FastAPI
from pydantic import BaseModel

from src.chat.chat_service import get_ai_response

app = FastAPI(title="AI Agent Pro", version="1.0.0")


class ChatRequest(BaseModel):
    username: str
    message: str


@app.get("/")
def home():
    return {"message": "AI Agent Pro is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = get_ai_response(
        username=request.username,
        message=request.message,
    )

    return {"response": response}

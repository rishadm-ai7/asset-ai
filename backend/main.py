import asyncio
from typing import AsyncIterable
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel, Field
from openai import OpenAI
 
# Create the app object
app = FastAPI()
 
# CORS setup
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# OpenAI client
openai_client = OpenAI(api_key=config("OPENAI_API_KEY"))
 
# Message history
app.message_history = []
 
# Message history model
class MessageHistoryModel(BaseModel):
    message: str = Field(title="Message")
 
# Chat form model
class ChatForm(BaseModel):
    chat: str = Field(title=" ", max_length=1000)
 
@app.post("/api/chat")
async def chat_endpoint(form: ChatForm):
    prompt = form.chat
    if not prompt:
        return {"error": "Prompt is empty"}
 
    response = await ai_response_generator(prompt)
    return response
 
# SSE endpoint
@app.get("/api/sse/{prompt}")
async def sse_ai_response(prompt: str) -> StreamingResponse:
    if not prompt:
        return StreamingResponse(empty_response(), media_type="text/event-stream")
    return StreamingResponse(ai_response_generator(prompt), media_type="text/event-stream")
 
# Empty response generator
async def empty_response() -> AsyncIterable[str]:
    yield ""
    while True:
        await asyncio.sleep(10)
 
async def ai_response_generator(prompt: str) -> dict:
    system_message = "You are a helpful assistant."
    prompt_template = "Previous messages:\n"
    for message_history in app.message_history:
        prompt_template += message_history.message + "\n"
    prompt_template += f"Human: {prompt}"
 
    openai_messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt_template},
    ]
 
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=openai_messages
    )
 
    chat_content = response.choices[0].message.content
 
    user_message = MessageHistoryModel(message=f"User: {prompt}")
    assistant_message = MessageHistoryModel(message=f"Chatbot: {chat_content}")
    app.message_history.append(user_message)
    app.message_history.append(assistant_message)
 
    return {"user_message": user_message.message, "assistant_message": assistant_message.message}
 
@app.get("/")
async def serve_frontend():
    with open("frontend/build/index.html") as f:
        return HTMLResponse(f.read())
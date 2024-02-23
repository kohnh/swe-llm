from typing import Union, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from openai import OpenAI
import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie
from urllib.parse import quote_plus

#Schemas
class APIError(BaseModel):
    code: int
    message: str
    request: Optional[dict]
    details: Optional[dict]


class Prompt(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    id: str = Field(readonly=True)
    name: str = Field(max_length=200)
    params: Optional[dict]
    tokens: Optional[int] = Field(ge=0, readonly=True)


class ConversationFull(Conversation):
    messages: List[Prompt]


class ConversationPOST(BaseModel):
    name: str = Field(max_length=200)
    params: Optional[dict]


class ConversationPUT(BaseModel):
    name: str = Field(max_length=200)
    params: Optional[dict]


# OpenAI
load_dotenv()
openAI_client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"


# FastAPI
app = FastAPI()


# MongoDB
username = quote_plus(os.environ.get("USERNAME"))
password = quote_plus(os.environ.get("PASSWORD"))
#change the uri to your own
uri = 'mongodb+srv://' + username + ':' + password + '@cluster0.duu8e7a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
beanie_client = AsyncIOMotorClient(uri)
init_beanie(database=beanie_client.db_name, document_models=[Conversation])
async def connect_to_mongodb():
    client = AsyncIOMotorClient(uri)
    await init_beanie(database="conversations", client=client)

# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/conversations", response_model=Conversation)
async def create_conversation(conversation: ConversationPOST):
    conversation = Conversation(**conversation.dict())
    await conversation.insert()
    return conversation

@app.get("/conversations", response_model=List[Conversation])
async def get_conversations():
    conversations = await Conversation.all()
    return conversations

@app.put("/conversations/{id}")
async def update_conversation(id: str, conversation: ConversationPUT):
    conversation = await Conversation.get(id)
    if conversation:
        conversation.name = conversation.name
        conversation.params = conversation.params
        await conversation.save()
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.get("/conversations/{id}", response_model=ConversationFull)
async def get_conversation(id: str):
    conversation = await Conversation.get(id)
    if conversation:
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.delete("/conversations/{id}")
async def delete_conversation(id: str):
    conversation = await Conversation.get(id)
    if conversation:
        await conversation.delete()
        return {"message": "Conversation deleted successfully"}
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.post("/queries", response_model=Prompt)
def create_prompt(prompt: Prompt):
    response = openAI_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": prompt.role, "content": prompt.content}],
        temperature=0,
    )
    return (response.choices[0].message.content)


# Connect to MongoDB when the application starts
@app.on_event("startup")
async def startup_event():
    await connect_to_mongodb()
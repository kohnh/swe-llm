from typing import Union, List, Optional

from fastapi import FastAPI
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

load_dotenv()
openAI_client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"


app = FastAPI()




username = quote_plus(os.environ.get("USERNAME"))
password = quote_plus(os.environ.get("PASSWORD"))
uri = 'mongodb+srv://' + username + ':' + password + '@cluster0.duu8e7a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
beanie_client = AsyncIOMotorClient(uri)
init_beanie(database=beanie_client.db_name, document_models=[Conversation])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/conversations", response_model=Conversation)
def create_conversation(conversation: ConversationPOST):
    response = openAI_client.chat.completions.create(
        model=MODEL,
        messages=[],
        temperature=0,
    )
    return (response.choices[0].message.content)

@app.get("/conversations", response_model=List[Conversation])
def get_conversations():
    return []

@app.put("/conversations/{id}")
def update_conversation(id: str, conversation: ConversationPUT):
    pass

@app.get("/conversations/{id}", response_model=ConversationFull)
def get_conversation(id: str):
    return ConversationFull(id=id, name="Dummy Conversation", params={}, tokens=100, messages=[])

@app.delete("/conversations/{id}")
def delete_conversation(id: str):
    pass

@app.post("/queries", response_model=Prompt)
def create_prompt(prompt: Prompt):
    return prompt
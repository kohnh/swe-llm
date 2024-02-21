from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from openai import OpenAI
import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie
from urllib.parse import quote_plus


load_dotenv()
openAI_client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"


app = FastAPI()


class Convo(BaseModel):
    name: str
    params: dict

username = quote_plus(os.environ.get("USERNAME"))
password = quote_plus(os.environ.get("PASSWORD"))
uri = 'mongodb+srv://' + username + ':' + password + '@cluster0.duu8e7a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
beanie_client = AsyncIOMotorClient(uri)
init_beanie(database=beanie_client.db_name, document_models=[Convo])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/conversations")
def Creates_a_new_conversation_with_a_LLM_model(convo: Convo | None = None):
    response = openAI_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ],
        temperature=0,
    )
    return (response.choices[0].message.content)
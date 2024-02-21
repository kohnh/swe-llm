from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

app = FastAPI()


class Convo(BaseModel):
    name: str
    params: dict


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/conversations")
def Creates_a_new_conversation_with_a_LLM_model(convo: Convo | None = None):
    response = client.chat.completions.create(
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
    return {"name": "string", "params": {
    "additionalProp1": {},
    },
    "additionalProp1": {}
    }
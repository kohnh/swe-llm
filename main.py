from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Convo(BaseModel):
    name: str
    params: dict


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/conversations")
def Creates_a_new_conversation_with_a_LLM_model(convo: Convo | None = None):
    return {"name": "string", "params": {
    "additionalProp1": {},
    },
    "additionalProp1": {}
    }
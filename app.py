from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import BraveSearch
import json
import os

searcher = BraveSearch.from_api_key(api_key='', search_kwargs={"count": 3})
model = ChatGroq(model_name='llama3-70b-8192', api_key='')

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant! Format your responses with headings and bullet points where appropriate."),
    ("human", "{input}")
])

chain = prompt | model

app = FastAPI()

class Prompt(BaseModel):
    prompt: str = None

async def generate_responses(input_text: str):
    search_results = searcher.run(input_text)
    search_results = json.loads(search_results)
    context = [result['snippet'] for result in search_results]
    context = ' '.join(context)
    input_text = input_text + "\n\nUse this context:\n\n" + context
    async for event in chain.astream_events(input_text, version="v1"):
        if event['event'] == 'on_chain_stream':
            yield event['data']['chunk'].content

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response_stream = generate_responses(data)
            async for response in response_stream:
                await websocket.send_text(response)
    except Exception as e:
        await websocket.close()

@app.get("/")
async def get():
    with open("index.html") as f:
        return HTMLResponse(f.read())

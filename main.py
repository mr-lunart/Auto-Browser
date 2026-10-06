import asyncio
from pydantic import BaseModel
from fastapi import FastAPI
from src.graphflow.Config import CONFIG 
from src.graphflow.MainGraph import GraphFlow 
from src.graphflow.RetrivalGraph import RetrivalGraph 

app = FastAPI()

graph_object = GraphFlow(CONFIG)
retrival_object = RetrivalGraph(CONFIG)
graph = graph_object.load_graph()
graph_retrival = retrival_object.load_graph()
graphflow = graph_object.compile_graph(graph)
retrivalflow = retrival_object.compile_graph(graph_retrival)

class Request(BaseModel):
    query: str = ""
    thread_id: str = None

async def send_message(config, question):
    graph_param = {
        "config": config,
        "messages": question,
    }
    output_graph = await graphflow.ainvoke(graph_param, config)
    return output_graph

async def send_query(config, question):
    graph_param = {
        "config": config,
        "messages": question,
    }
    output_graph = await retrivalflow.ainvoke(graph_param, config)
    return output_graph

@app.post("/run_chatbot")
async def run_chatbot(request:Request):
    query = request.query
    thread_id = request.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    # send message to LLM
    response = await send_message(config, query)
    return response

@app.post("/run_query")
async def run_query(request:Request):
    query = request.query
    thread_id = request.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    # send message to LLM
    response = await send_query(config, query)
    return response

if __name__ == "__main__":
    # requested_schema = """
    #     NeoChip’s (NC) shares surged in their first week of trading on the NewTech Exchange. 
    #     However, market analysts caution that the chipmaker’s public debut may
    #     not reflect trends for other technology IPOs. NeoChip, previously a private entity,
    #     was acquired by Quantum Systems in 2016. The innovative semiconductor firm
    #     specializes in low-power processors for wearables and IoT devices.
    #     """
    # request = Request(
    #     query=requested_schema,
    #     thread_id="002"
    # )
    # hasil = asyncio.run(run_chatbot(request))

    requested_schema = """
        NeoChip's shares soared so much in their first week — what a debut
        NeoChip's shares surged in their first week of trading on the NewTech Exchange.
        Can you review NeoChip's trading performance before comparing it to other technology IPOs.
        Did NeoChip's strong debut on the NewTech Exchange reflect broader trends in technology IPOs
        What is connection between Quantum System and Neochip and NewTech Exchange
        can you tell me what is the today weather
        what is that
        stop
        you looks pretty today.
        """
    
    requested_schema = """
        Hi i want noodles recipe, do you have good recom
        """

    # request = Request(
    #     query=requested_schema,
    #     thread_id="002"
    # )
    # hasil = asyncio.run(run_query(request))

    request = Request(
        query=requested_schema,
        thread_id="002"
    )
    hasil = asyncio.run(run_chatbot(request))
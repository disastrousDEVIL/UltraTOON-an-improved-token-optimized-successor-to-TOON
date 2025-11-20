from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph_runner
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

class BenchmarkRequest(BaseModel):
    data: dict
    question: str

@app.post("/run")
async def run_benchmark(request: BenchmarkRequest):
    result=graph_runner(req.data,req.question)
    return result

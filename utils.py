import time
from langchain_openai import ChatOpenAI
from lagsmith.wrappers import wrap_openai
import numpy as np

llm=wrap_openai(ChatOpenAI(model="gpt-4o-mini",temperature=0))

def run_llm(question:str,context:str):
    """Sends a Real prompt to LLM:
    DATA:
    <json or toon>

    QUESTION:
    <question>

    Returns:
    - asnwer (string)
    - latency (seconds)
    - usage (prompt_tokens,completion_tokens,total_tokens)
    """

    prompt:f"DATA: \n{context}\n\nQUESTION:\n{question}"

    start_time=time.time()
    response=llm.invoke(prompt)
    latency=time.time()-start_time
    
    usage=response.response_metadata.get("token_usage",{})

    return response.content,latency,usage

def evaluate_quality(ans_json:str,ans_toon:str,ans_ultra:str):
    """
    Very lightweight evaluation:
    Compares the lengths of asnwers as a proxy for similarity.
    You can later upgrade this to embeddings or ROUGE"""

    def score(a,b):
        if len(a)==0 or len(b)==0:
            return 0
        return 1-abs(len(a)-len(b))/max(len(a),1)

    return{
        "json_vs_toon":score(ans_json,ans_toon),
        "json_vs_ultra":score(ans_json,ans_ultra),
        "toon_vs_ultra":score(ans_toon,ans_ultra)
    }
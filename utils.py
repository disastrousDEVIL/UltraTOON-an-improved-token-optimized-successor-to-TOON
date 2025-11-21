import time
from langchain_openai import ChatOpenAI
from langsmith import traceable

# Correct OpenAI LangChain model
llm = ChatOpenAI(
    model="gpt-5-nano-2025-08-07",
    temperature=0
)

@traceable  # This enables LangSmith tracing for this function
def run_llm(question: str, context: str):
    """
    Sends a REAL prompt to the LLM and returns:
    - answer content
    - latency
    - true token usage (prompt + completion)
    """

    prompt = f"DATA:\n{context}\n\nQUESTION:\n{question}"

    start = time.time()
    response = llm.invoke(prompt)
    latency = time.time() - start

    usage = response.response_metadata.get("token_usage", {})

    return response.content, latency, usage


def evaluate_quality(ans_json: str, ans_toon: str, ans_ultra: str):
    """Simple length similarity measure."""
    def score(a, b):
        if not a or not b:
            return 0
        return 1 - abs(len(a) - len(b)) / max(len(a), 1)

    return {
        "json_vs_toon": score(ans_json, ans_toon),
        "json_vs_ultra": score(ans_json, ans_ultra),
        "toon_vs_ultra": score(ans_toon, ans_ultra)
    }

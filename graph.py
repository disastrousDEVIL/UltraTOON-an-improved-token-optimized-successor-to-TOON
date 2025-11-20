from converters import json_to_toon, json_to_ultra_toon
from utils import run_llm, evaluate_quality

def graph_runner(json_data, question):
    """
    Correct benchmarking pipeline:
    1. Convert JSON → TOON + UltraTOON
    2. Send JSON prompt into LLM → record real token usage
    3. Send TOON prompt into LLM → record real token usage
    4. Send UltraTOON prompt into LLM → record real token usage
    """

    # Convert once at the top
    pure_toon = json_to_toon(json_data)
    ultra_toon = json_to_ultra_toon(json_data)
    json_str = str(json_data)

    # Run LLM with JSON
    ans_json, lat_json, usage_json = run_llm(question, json_str)

    # Run LLM with pure TOON
    ans_toon, lat_toon, usage_toon = run_llm(question, pure_toon)

    # Run LLM with ultra TOON
    ans_ultra, lat_ultra, usage_ultra = run_llm(question, ultra_toon)

    # Evaluate answer quality differences
    quality = evaluate_quality(ans_json, ans_toon, ans_ultra)

    # Extract true token counts from LangSmith logs:
    tokens_json = usage_json.get("prompt_tokens", 0) + usage_json.get("completion_tokens", 0)
    tokens_toon = usage_toon.get("prompt_tokens", 0) + usage_toon.get("completion_tokens", 0)
    tokens_ultra = usage_ultra.get("prompt_tokens", 0) + usage_ultra.get("completion_tokens", 0)

    return {
        "tokens": {
            "json": tokens_json,
            "toon": tokens_toon,
            "ultra": tokens_ultra
        },
        "prompt_tokens": {
            "json": usage_json.get("prompt_tokens", 0),
            "toon": usage_toon.get("prompt_tokens", 0),
            "ultra": usage_ultra.get("prompt_tokens", 0)
        },
        "latency": {
            "json": lat_json,
            "toon": lat_toon,
            "ultra": lat_ultra
        },
        "usage_raw": {
            "json": usage_json,
            "toon": usage_toon,
            "ultra": usage_ultra
        },
        "answers": {
            "json": ans_json,
            "toon": ans_toon,
            "ultra": ans_ultra
        },
        "quality_scores": quality
    }

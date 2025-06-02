import os
import asyncio
import random
import runpod
from utils import JobInput
from engine import vLLMEngine, OpenAIvLLMEngine

# Initialize engines once
_vllm_engine = vLLMEngine()
_openai_engine = OpenAIvLLMEngine(_vllm_engine)

# ---- Handlers ----

# Async default handler (streams output)
async def async_handler(job):
    job_input = JobInput(job["input"])
    engine = _openai_engine if job_input.openai_route else _vllm_engine
    async for output in engine.generate(job_input):
        yield output

# Sync generator handler (simple dummy example)
def generator_handler(job):
    for i in range(3):
        runpod.serverless.progress_update(job, f"Progress: {i+1}/3")
        yield f"Generated output {i+1}"

# Concurrency adjusting handler with dynamic concurrency modifier
def concurrency_handler(job):
    runpod.serverless.progress_update(job, "Starting concurrency handler")
    # Simulate some work
    for i in range(2):
        yield f"Concurrency handler step {i+1}"
        runpod.serverless.progress_update(job, f"Step {i+1}/2 complete")

def adjust_concurrency(current_concurrency):
    """Dynamically adjust concurrency based on simulated load."""
    # Simulate changing request rate (in real use, hook to metrics)
    request_rate = random.randint(20, 100)
    max_concurrency = 10
    min_concurrency = 1
    threshold = 50

    if request_rate > threshold and current_concurrency < max_concurrency:
        return current_concurrency + 1
    elif request_rate <= threshold and current_concurrency > min_concurrency:
        return current_concurrency - 1
    return current_concurrency

# ---- Handler selection ----
HANDLER_TYPE = os.getenv("HANDLER_TYPE", "DEFAULT").upper()

if HANDLER_TYPE == "GENERATOR":
    selected_handler = generator_handler
    concurrency_mod = None  # No concurrency mod for sync generator example

elif HANDLER_TYPE == "CONCURRENCY":
    selected_handler = concurrency_handler
    concurrency_mod = adjust_concurrency

else:
    # Default async handler
    selected_handler = async_handler
    concurrency_mod = lambda _: _vllm_engine.max_concurrency

# ---- Runpod start ----
runpod.serverless.start(
    {
        "handler": selected_handler,
        "concurrency_modifier": concurrency_mod,
        "return_aggregate_stream": True,
    }
)

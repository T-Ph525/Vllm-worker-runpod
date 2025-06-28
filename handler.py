import runpod
import torch
import logging
from utils import JobInput
from engine import vLLMEngine, OpenAIvLLMEngine
import random

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)

# --- Device Info ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.info(f"Running on device: {device}")

# --- Load Engines Once ---
_vllm_engine = vLLMEngine()
_openai_engine = OpenAIvLLMEngine(_vllm_engine)

# --- Async Streaming Handler with Progress Updates + Auto Refresh ---
async def async_handler(job):
    try:
        runpod.serverless.progress_update(job, "Job received. Parsing input...")

        job_input = JobInput(job["input"])
        engine = _openai_engine if job_input.openai_route else _vllm_engine

        runpod.serverless.progress_update(job, "Starting generation...")

        results = []
        async for output in engine.generate(job_input):
            results.append(output)
            runpod.serverless.progress_update(job, f"Generated chunk {len(results)}")

        runpod.serverless.progress_update(job, "Generation complete. Returning results...")

        return {
            "job_results": results,
            "refresh_worker": True  # Force worker restart to free memory
        }

    except Exception as e:
        logging.exception("Handler error:")
        return {
            "error": str(e),
            "refresh_worker": True  # Restart even on failure
        }

# --- Concurrency Modifier (Optional) ---
def adjust_concurrency(current_concurrency):
    request_rate = random.randint(20, 100)
    max_concurrency = 10
    min_concurrency = 1
    threshold = 50

    if request_rate > threshold and current_concurrency < max_concurrency:
        return current_concurrency + 1
    elif request_rate <= threshold and current_concurrency > min_concurrency:
        return current_concurrency - 1
    return current_concurrency

# --- Start RunPod Serverless ---
runpod.serverless.start({
    "handler": async_handler,
    "concurrency_modifier": adjust_concurrency,
    "return_aggregate_stream": True
})

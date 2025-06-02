import os
import runpod
import asyncio
import random

# ========== Basic Default Handler ==========
def basic_handler(job):
    job_input = job["input"]  # Access the input from the request
    # Add your custom code here
    return "Your job results"

def basic_concurrency_modifier(current_concurrency):
    # Simple fixed concurrency modifier for basic handler
    return 5

# ========== Generator Handler ==========
def generator_handler(job):
    for count in range(3):
        runpod.serverless.progress_update(job, f"Update {count + 1}/3")
        yield f"This is the {count} generated output."

def generator_concurrency_modifier(current_concurrency):
    # Fixed concurrency for generator handler
    return 3

# ========== Concurrency Handler ==========
# Global variable to simulate a varying request rate
request_rate = 0

def update_request_rate():
    global request_rate
    request_rate = random.randint(20, 100)

async def concurrency_handler(job):
    job_input = job["input"]
    delay = job_input.get("delay", 1)
    await asyncio.sleep(delay)
    return f"Processed: {job_input}"

def concurrency_concurrency_modifier(current_concurrency):
    global request_rate
    update_request_rate()

    max_concurrency = 10
    min_concurrency = 1
    high_request_rate_threshold = 50

    if request_rate > high_request_rate_threshold and current_concurrency < max_concurrency:
        return current_concurrency + 1
    elif request_rate <= high_request_rate_threshold and current_concurrency > min_concurrency:
        return current_concurrency - 1
    return current_concurrency

# ========== Async Handler ==========
async def async_handler(job):
    for i in range(5):
        output = f"Generated async token output {i}"
        yield output
        await asyncio.sleep(1)

def async_concurrency_modifier(current_concurrency):
    # Fixed concurrency for async handler
    return 4

# ========== Handler selection ==========
HANDLER_TYPE = os.getenv("HANDLER_TYPE", "").upper()

if HANDLER_TYPE == "GENERATOR":
    selected_handler = generator_handler
    concurrency_modifier = generator_concurrency_modifier

elif HANDLER_TYPE == "CONCURRENCY":
    selected_handler = concurrency_handler
    concurrency_modifier = concurrency_concurrency_modifier

elif HANDLER_TYPE == "ASYNC":
    selected_handler = async_handler
    concurrency_modifier = async_concurrency_modifier

else:
    # Default to basic handler
    selected_handler = basic_handler
    concurrency_modifier = basic_concurrency_modifier

runpod.serverless.start({
    "handler": selected_handler,
    "concurrency_modifier": concurrency_modifier,
    "return_aggregate_stream": True
})

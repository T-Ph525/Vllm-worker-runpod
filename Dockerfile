FROM runpod/worker-v1-vllm:v2.5.0stable-cuda12.1.0

# Define environment variable (corrected syntax)
ENV MODEL_NAME="NeverSleep/Lumimaid-v0.2-12B"
ENV HF_HOME="/app/tmp/hf_cache"

# Set working directory
WORKDIR /app

# Copy model download scripts
COPY download_model.py utils.py ./

# Install required package
RUN pip install --no-cache-dir huggingface_hub

# Download the model (this executes at build time)
RUN python3 download_model.py

# Default CMD can still start the vLLM server (if needed)
# You may override this via `runpod.template` or docker run CMD
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "/"]

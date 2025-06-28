FROM runpod/worker-v1-vllm:v2.5.0stable-cuda12.1.0

ENV MODEL_NAME=""
ENV HF_HOME="/app/tmp/hf_cache"

WORKDIR /

# Copy model download scripts and your custom handler
COPY download_model.py utils.py handler.py .

RUN pip install --no-cache-dir huggingface_hub

# Download the model during build
RUN python3 download_model.py

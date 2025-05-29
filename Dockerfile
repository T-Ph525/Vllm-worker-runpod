FROM runpod/worker-v1-vllm:v2.5.0stable-cuda12.1.0

# Set working directory
WORKDIR /app

# Copy your scripts
COPY download_model.py utils.py ./

# Install required Python packages
RUN pip install --no-cache-dir huggingface_hub

# Set default env vars (can be overridden at runtime)
ENV HF_HOME=/app/tmp/hf_cache
# Run script using user-provided env vars
CMD ["python", "download_model.py"]

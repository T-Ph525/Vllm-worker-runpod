FROM runpod/worker-v1-vllm:v2.5.0stable-cuda12.1.0

# Set environment variables
ENV HF_HOME="/app/tmp/hf_cache"

# Set working directory
WORKDIR /app

# Copy your files into the image
COPY download_model.py utils.py handler.py ./

# Install required dependencies
RUN pip install --no-cache-dir huggingface_hub

# Download the model using the environment variable
RUN python3 download_model.py

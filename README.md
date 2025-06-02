# VLLM Worker for RunPod (with Pre-Download Support)

This repo provides a custom VLLM worker Docker image for RunPod with **model pre-download** functionality using `MODEL_NAME` and related environment variables.

> 🛠️ The main motivation is to **avoid the 3–5 minute delay** caused by RunPod’s default VLLM image downloading model weights during the first request.
>
> Instead, this image **downloads the model at startup**, so your inference API is **ready instantly** after the container spins up.

---

## ✅ Features

* 🚀 **Downloads model and tokenizer at container startup**
* 📦 Supports `.safetensors`, `.bin`, `.pt`
* 🔐 Optional Hugging Face token support for private/gated models
* ⚡ Generates `local_model_args.json` for VLLM to use
* 🧼 Fully cacheable via `HF_HOME`

---

## 🧠 Why Use This?

By default, RunPod’s VLLM worker pulls model weights from Hugging Face **at inference time** — meaning the **first API call can take up to 4 minutes** for large models.

This image avoids that entirely by:

* Downloading the model when the container starts
* Caching it in `/models` or any `HF_HOME` you define
* Passing the resolved local path to the VLLM server

---

## 🔧 Environment Variables

| Variable             | Description                                                             | Required |
| -------------------- | ----------------------------------------------------------------------- | -------- |
| `MODEL_NAME`         | Hugging Face model repo name (e.g. `TheBloke/Mistral-7B-Instruct-v0.1`) | ✅        |
| `MODEL_REVISION`     | Optional Git revision (`main`, commit SHA, etc.)                        | ❌        |
| `TOKENIZER_NAME`     | Optional tokenizer repo name                                            | ❌        |
| `TOKENIZER_REVISION` | Optional tokenizer revision                                             | ❌        |
| `HF_TOKEN`           | Hugging Face token for private/gated models                             | ❌        |
| `HF_HOME`            | Hugging Face cache/download directory (default: `/models`)              | ✅        |

---

## 🐳 Usage

**1. Build:**

```bash
docker build -t vllm-runpod .
```

**2. Run (example with Mistral):**

```bash
docker run --rm \
  -e MODEL_NAME=TheBloke/Mistral-7B-Instruct-v0.1 \
  -e HF_HOME=/models \
  vllm-runpod
```

---

## 🧰 Dockerfile CMD

```dockerfile
CMD ["bash", "-c", "python /workspace/download_model.py && python3 -m vllm.entrypoints.openai.api_server --model /"]
```

This:

1. Runs the downloader script (`download_model.py`) with `MODEL_NAME`
2. Starts VLLM using the downloaded model path

---

## 📦 Output

* ✅ Model and tokenizer downloaded to `$HF_HOME`
* 🧾 `local_model_args.json` written with actual paths
* ⚡ VLLM API starts immediately with no cold download

---

## 📝 Note

This repo uses the same `download_model.py` logic as RunPod’s official workers, but gives you more control via `Dockerfile` and environment.
It may be deprecated if future versions of RunPod’s base VLLM image support pre-downloading natively.

---

## 🙏 Credits

* Based on [RunPod’s vllm-worker](https://github.com/runpod-workers/vllm-worker)
* Model downloading via [huggingface\_hub](https://github.com/huggingface/huggingface_hub)

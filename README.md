# VLLM Worker for RunPod

This repository provides a minimal serverless-compatible VLLM worker setup for RunPod, with support for dynamic Hugging Face model downloading via environment variables.

> ⚠️ **Note:** This is essentially a wrapper around RunPod’s base VLLM Docker image with the added ability to specify a custom model through the `MODEL_NAME` environment variable. The `download_model.py` logic is derived from RunPod’s own model downloader and may be deprecated if their base repo includes the same functionality in the future.

---

## 🚀 Features

* ✅ Dynamic model downloading using `huggingface_hub`
* ✅ Supports `.safetensors`, `.bin`, `.pt` model formats
* ✅ Auto-downloads both model and tokenizer (if separate)
* ✅ Optional HF token authentication via `HF_TOKEN`
* ✅ Generates `local_model_args.json` for downstream usage

---

## 🧱 Environment Variables

| Variable             | Description                                                             | Required |
| -------------------- | ----------------------------------------------------------------------- | -------- |
| `MODEL_NAME`         | Hugging Face model repo name (e.g. `TheBloke/Mistral-7B-Instruct-v0.1`) | ✅        |
| `MODEL_REVISION`     | Optional Git revision (`main`, commit SHA, etc.)                        | ❌        |
| `TOKENIZER_NAME`     | Optional separate tokenizer repo name                                   | ❌        |
| `TOKENIZER_REVISION` | Optional tokenizer revision                                             | ❌        |
| `HF_HOME`            | Cache/download directory for models and tokenizers                      | ✅        |
| `HF_TOKEN`           | Hugging Face token (for gated/private models)                           | ❌        |

---

## 🐳 Docker Usage

This Dockerfile:

* Installs dependencies
* Runs `download_model.py`
* Starts the VLLM OpenAI-compatible server

**Build image:**

```bash
docker build -t vllm-runpod .
```

**Run container:**

```bash
docker run --rm -e MODEL_NAME=TheBloke/Mistral-7B-Instruct-v0.1 -e HF_HOME=/models vllm-runpod
```

---

## 📂 Output

On successful startup, the following are generated inside your container:

* Downloaded model and tokenizer in `$HF_HOME`
* `local_model_args.json` with resolved model/tokenizer paths

---

## 📝 Example `CMD` in Dockerfile

```dockerfile
CMD ["bash", "-c", "python /workspace/download_model.py && python3 -m vllm.entrypoints.openai.api_server --model /"]
```

---

## 🔧 Notes

* Only `MODEL_NAME` is required. If tokenizer files are part of the model repo, separate `TOKENIZER_NAME` is not needed.
* Tensorization is stubbed but not enabled yet — you can enable it once VLLM supports tensorized model loading properly.

---

## 📦 Credits

* Based on [RunPod’s official vllm-worker](https://github.com/runpod-workers/vllm-worker).
* Hugging Face model handling via [`huggingface_hub`](https://github.com/huggingface/huggingface_hub).

# Super STT — Qwen3-ASR backend

[![coverage](https://img.shields.io/endpoint?url=https://jorge-menjivar.github.io/super-stt-qwen-asr/coverage.json)](https://jorge-menjivar.github.io/super-stt-qwen-asr/)

A speech-to-text backend for **[Super STT](https://github.com/jorge-menjivar/super-stt)**.
It runs [Qwen3-ASR](https://huggingface.co/Qwen) models locally — on CPU or a
CUDA GPU — to turn speech into text.

Super STT is an on-device speech-to-text engine. It doesn't ship any models of
its own — it loads **backends** like this one at runtime. This repo packages the
Qwen3-ASR family (0.6B and 1.7B) as one of those backends.

## Using it

You don't run this directly. Super STT discovers it through its backend
registry, downloads a prebuilt release for your platform, fetches the model
weights, and runs it sandboxed. To use Qwen3-ASR, install Super STT and enable
it from the app — see the [Super STT docs](https://github.com/jorge-menjivar/super-stt).

## Models

Chosen by `name` when Super STT loads the backend. Each runs on CPU or a CUDA
GPU; weights are pulled from Hugging Face on first load. Both are multilingual
(30 languages). `~VRAM` is the GPU memory the model is expected to use.

| Model (`name`)   | Upstream model                                                    | Device     | ~VRAM   |
| ---------------- | ----------------------------------------------------------------- | ---------- | ------- |
| `qwen3-asr-0.6b` | [Qwen/Qwen3-ASR-0.6B](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) | CPU / CUDA | ~2.5 GB |
| `qwen3-asr-1.7b` | [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | CPU / CUDA | ~6 GB   |

## What's in here

A small, self-contained Python program (Starlette over a Unix socket) that loads
a Qwen3-ASR model and speaks the Super STT backend protocol (a tiny HTTP API over
a Unix socket). It shares no code with the Super STT project.

Releases ship as a **relocatable bundle** — a standalone CPython plus every
dependency (PyTorch, qwen-asr, …) — so the host needs no Python installed.

## Building from source

Most people never need to — Super STT downloads prebuilt releases. For
development you need [uv](https://docs.astral.sh/uv/) and
[`just`](https://github.com/casey/just):

```bash
just sync          # set up the dev environment
just ci            # lint, format-check, type-check, and test
just coverage      # the above with an HTML coverage report under htmlcov/
```

Assemble a release bundle (downloads PyTorch; the CUDA bundle is large):

```bash
just bundle cpu      # CPU bundle    -> target/
just bundle cuda13   # CUDA bundle   -> target/
```

The dev environment deliberately omits the heavy ML stack (PyTorch, qwen-asr):
the tests drive a fake engine and never import it, so they stay fast and need no
GPU. The real stack is provisioned only inside the shipped bundle.

## License

GPL-3.0-only.

# Super STT — Qwen3-ASR backend (transformers)

[![coverage](https://img.shields.io/endpoint?url=https://jorge-menjivar.github.io/super-stt-qwen-asr/coverage.json)](https://jorge-menjivar.github.io/super-stt-qwen-asr/)

A speech-to-text backend for **[Super STT](https://github.com/jorge-menjivar/super-stt)**.
It runs [Qwen3-ASR](https://huggingface.co/Qwen) models locally — on CPU or a
CUDA GPU — to turn speech into text, through PyTorch and Hugging Face
[transformers](https://github.com/huggingface/transformers) by way of Qwen's
`qwen-asr` package.

> [!TIP]
> **You probably want [super-stt-qwen](https://github.com/super-libre/super-stt-qwen)
> instead.** It runs the same models, ported to Rust on
> [Burn](https://github.com/tracel-ai/burn), and is listed in Super STT as a
> separate backend, also named Qwen, whose description says it runs on Burn.
> Against this one:
>
> - **Faster on a GPU.** On an RTX 3090, in bf16, the median transcription of
>   an 11-second clip took 0.14 s there against 0.66 s here with the 0.6B
>   model, and 0.24 s against 0.62 s with the 1.7B; a two-minute clip took
>   1.3 s against 4.8 s, and 2.0 s against 5.2 s. Most of the difference is
>   per-token overhead: here each decoding step is driven from Python, there it
>   is replayed as one captured GPU graph. On clips over eight seconds the
>   encoder also does less work there, attending within eight-second windows
>   as the model's own vLLM backend does, where `transformers`' default
>   attention covers the whole clip.
> - **More hardware.** Builds for CUDA, ROCm, Vulkan, Metal and the CPU, on
>   x86_64 and ARM Linux and on macOS. This one ships CUDA and CPU builds for
>   x86_64 Linux.
> - **One small binary** instead of a multi-gigabyte bundle with a Python
>   interpreter and PyTorch.
> - **More of the backend contract.** Streamed previews while a clip is
>   decoded (this one sends the text only at the end), a cancel that stops a
>   transcription (here it is acknowledged but the transcription runs on), and
>   a language chosen by the user (here the daemon's code, `en`, reaches
>   `qwen-asr` as `En`, which it rejects, so the request fails).
>
> What it costs: its first load of each model compiles and tunes GPU kernels,
> about six minutes on CUDA and two on Vulkan on that RTX 3090, where a load
> here takes seconds; later loads take four to nine seconds. The 1.7B model
> holds 7.6 GiB of GPU memory there against at most 5.8 GiB here. And on the
> CPU it is no faster: 4.9 s for the 11-second clip, against 4.2 to 5.1 s for
> this backend's bf16 build.
>
> This repository stays as the reference for running a `transformers` model
> under Super STT. Both backends can be installed side by side; nothing moves
> from one to the other.

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
a Qwen3-ASR model through `transformers` and speaks the Super STT backend
protocol (a tiny HTTP API over a Unix socket). It shares no code with the Super
STT project.

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

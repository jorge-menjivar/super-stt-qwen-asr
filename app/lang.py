# SPDX-License-Identifier: GPL-3.0-only
"""Language codes, from what the daemon sends to what the model was trained on.

The daemon sends a BCP-47 tag (``en``, ``zh-CN``, …) narrowed to the model's
declared ``supported_languages``, or the reserved :data:`AUTO`. Qwen3-ASR names
its languages in English instead — ``English``, ``Chinese`` — and ``qwen_asr``
accepts nothing else: handed ``en``, it capitalizes it to ``En``, finds no such
language, and raises. This module is the join between the two, and the reason
``backend.toml`` can declare ordinary language codes rather than leaking the
model's vocabulary into the settings UI.

Regional subtags are dropped: the model has one Chinese and one Portuguese, so
``zh-CN`` and ``zh-TW`` both resolve to ``Chinese``. Cantonese is its own
language to the model, and is reached by its own code, ``yue``.

The table is the Rust backend's (super-stt-qwen) ``src/lang.rs``, value for
value, so a request reaches both backends as the same prompt.
"""

from __future__ import annotations

LANGUAGES: tuple[tuple[str, str], ...] = (
    ("zh", "Chinese"),
    ("en", "English"),
    ("yue", "Cantonese"),
    ("ar", "Arabic"),
    ("de", "German"),
    ("fr", "French"),
    ("es", "Spanish"),
    ("pt", "Portuguese"),
    ("id", "Indonesian"),
    ("it", "Italian"),
    ("ko", "Korean"),
    ("ru", "Russian"),
    ("th", "Thai"),
    ("vi", "Vietnamese"),
    ("ja", "Japanese"),
    ("tr", "Turkish"),
    ("hi", "Hindi"),
    ("ms", "Malay"),
    ("nl", "Dutch"),
    ("sv", "Swedish"),
    ("da", "Danish"),
    ("fi", "Finnish"),
    ("pl", "Polish"),
    ("cs", "Czech"),
    ("fil", "Filipino"),
    ("fa", "Persian"),
    ("el", "Greek"),
    ("ro", "Romanian"),
    ("hu", "Hungarian"),
    ("mk", "Macedonian"),
)
"""The thirty languages Qwen3-ASR transcribes, as ``(BCP-47 primary subtag,
model name)``, in the order the checkpoints' ``support_languages`` lists them.

The names are ``qwen_asr``'s own spelling. ``backend.toml`` declares the same
thirty codes for every model, and a test holds the two lists together.
"""

AUTO = "auto"
"""The reserved tag that asks for detection.

The contract says a backend must accept it and never answer it with
``unsupported_language``. Qwen3-ASR detects on its own when given no language,
so the caller passes ``None`` for it.
"""


def to_model_name(tag: str | None) -> str | None:
    """Translate a request's ``language`` to the name ``qwen_asr`` expects.

    Returns :data:`AUTO` for detection — ``auto`` itself, or an absent or blank
    field — and ``None`` for a tag the model does not transcribe, which the
    caller reports as ``unsupported_language``. Matching is on the primary
    subtag alone and is case-insensitive, so ``EN``, ``en`` and ``en-GB`` are
    one language.
    """
    if tag is None or not tag.strip():
        return AUTO
    primary = tag.strip().replace("_", "-").split("-", 1)[0].lower()
    if primary == AUTO:
        return AUTO
    for code, name in LANGUAGES:
        if primary == code:
            return name
    return None


def supported_codes() -> tuple[str, ...]:
    """Every BCP-47 code this backend accepts.

    Only the tests read it — the manifest carries its own copy of the list, and
    the test beside them is what holds the two together.
    """
    return tuple(code for code, _ in LANGUAGES)

# SPDX-License-Identifier: GPL-3.0-only
"""BCP-47 in, the model's own language name out."""

import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import lang

ROOT = Path(__file__).resolve().parents[1]

# qwen_asr's `SUPPORTED_LANGUAGES`, which is also every checkpoint's
# `support_languages`: a name here that the model does not know is one
# qwen_asr refuses. qwen_asr is bundle-only, so the list is copied.
MODEL_NAMES = [
    "Chinese",
    "English",
    "Cantonese",
    "Arabic",
    "German",
    "French",
    "Spanish",
    "Portuguese",
    "Indonesian",
    "Italian",
    "Korean",
    "Russian",
    "Thai",
    "Vietnamese",
    "Japanese",
    "Turkish",
    "Hindi",
    "Malay",
    "Dutch",
    "Swedish",
    "Danish",
    "Finnish",
    "Polish",
    "Czech",
    "Filipino",
    "Persian",
    "Greek",
    "Romanian",
    "Hungarian",
    "Macedonian",
]


def test_every_name_is_one_the_model_knows():
    assert [name for _, name in lang.LANGUAGES] == MODEL_NAMES


def test_the_manifest_declares_the_table():
    # Every model declares exactly the table's codes, and its
    # `primary_language` among them.
    manifest = tomllib.loads((ROOT / "backend.toml").read_text())
    codes = sorted(lang.supported_codes())
    assert len(manifest["models"]) == 2
    for model in manifest["models"]:
        assert sorted(model["supported_languages"]) == codes, model["name"]
        assert model["primary_language"] in codes, model["name"]


def test_codes_resolve_to_names():
    assert lang.to_model_name("en") == "English"
    assert lang.to_model_name("fr") == "French"
    assert lang.to_model_name("EN-gb") == "English"
    assert lang.to_model_name("zh_TW") == "Chinese"
    assert lang.to_model_name("yue") == "Cantonese"
    assert lang.to_model_name("fil") == "Filipino"


def test_auto_and_nothing_detect():
    assert lang.to_model_name("auto") == lang.AUTO
    assert lang.to_model_name("AUTO") == lang.AUTO
    assert lang.to_model_name(None) == lang.AUTO
    assert lang.to_model_name("  ") == lang.AUTO


def test_an_unknown_code_is_unsupported():
    assert lang.to_model_name("xx") is None
    assert lang.to_model_name("he") is None
    # A name is not a code.
    assert lang.to_model_name("English") is None

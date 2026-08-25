from __future__ import annotations

import json
import os
import re
from typing import Any, List

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)

ACTION_ITEMS_SCHEMA = {
    "type": "object",
    "properties": {
        "action_items": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["action_items"],
    "additionalProperties": False,
}


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _response_content(response: Any) -> Any:
    """Read content from both Ollama's object and dictionary responses."""
    if isinstance(response, dict):
        message = response.get("message", {})
        return message.get("content", "") if isinstance(message, dict) else ""
    message = getattr(response, "message", None)
    if isinstance(message, dict):
        return message.get("content", "")
    return getattr(message, "content", "") if message is not None else ""


def _parse_action_items(content: Any) -> List[str]:
    """Normalize a structured Ollama response into non-empty, unique strings."""
    if isinstance(content, str):
        value = content.strip()
        if value.startswith("```"):
            value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.IGNORECASE)
            value = re.sub(r"\s*```$", "", value)
        parsed = json.loads(value)
    else:
        parsed = content

    if isinstance(parsed, dict):
        parsed = parsed.get("action_items", parsed.get("items"))
    if not isinstance(parsed, list):
        raise ValueError("LLM response does not contain an action item list")

    normalized: List[str] = []
    seen: set[str] = set()
    for item in parsed:
        if isinstance(item, dict):
            item = item.get("text", "")
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        key = cleaned.casefold()
        if cleaned and key not in seen:
            seen.add(key)
            normalized.append(cleaned)
    return normalized


def extract_action_items_llm(text: str) -> List[str]:
    """Extract action items with Ollama, falling back to local rules on failure."""
    source = text.strip()
    if not source:
        return []

    # AI-assisted implementation: constrain the model with a JSON schema so the
    # API contract remains deterministic even though the extraction is semantic.
    try:
        response = chat(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract only concrete tasks that someone can act on. "
                        "Return each task as a concise string. Do not invent tasks."
                    ),
                },
                {"role": "user", "content": source},
            ],
            format=ACTION_ITEMS_SCHEMA,
            options={"temperature": 0},
        )
        return _parse_action_items(_response_content(response))
    except Exception:
        # Ollama may be unavailable or an older model may ignore the schema.
        return extract_action_items(source)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters

import re


TAG_PATTERN = re.compile(r"(?<![\w#])#([^\W#][\w-]*)", re.UNICODE)


def extract_action_items(text: str) -> list[str]:
    lines = [
        line.strip().lstrip("-* ").strip()
        for line in text.splitlines()
        if line.strip()
    ]
    return [
        line
        for line in lines
        if line.endswith("!") or line.lower().startswith("todo:")
    ]


def extract_tags(text: str) -> list[str]:
    """Return unique hashtags, without ``#``, in first-seen order."""
    return list(dict.fromkeys(match.group(1) for match in TAG_PATTERN.finditer(text)))


def extract_note(text: str) -> dict[str, list[str]]:
    """Extract all supported structured data from note text."""
    return {"action_items": extract_action_items(text), "tags": extract_tags(text)}

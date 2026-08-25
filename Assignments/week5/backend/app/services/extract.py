import re

HASHTAG_PATTERN = re.compile(r"(?<!\w)#([\w-]+)", re.UNICODE)
CHECKBOX_PATTERN = re.compile(r"^\s*-\s*\[\s\]\s+(.+?)\s*$", re.IGNORECASE)


def extract_hashtags(text: str) -> list[str]:
    """Return normalized, de-duplicated hashtags in source order."""
    return list(dict.fromkeys(match.lower() for match in HASHTAG_PATTERN.findall(text)))


def extract_action_items(text: str) -> list[str]:
    """Extract Markdown checkboxes plus the starter project's legacy action syntax."""
    items: list[str] = []
    for raw_line in text.splitlines():
        checkbox = CHECKBOX_PATTERN.match(raw_line)
        if checkbox:
            item = checkbox.group(1).strip()
        else:
            item = raw_line.strip().lstrip("-").strip()
            if not (item.endswith("!") or item.lower().startswith("todo:")):
                continue
        if item and item not in items:
            items.append(item)
    return items


def extract_content(text: str) -> dict[str, list[str]]:
    return {"tags": extract_hashtags(text), "action_items": extract_action_items(text)}

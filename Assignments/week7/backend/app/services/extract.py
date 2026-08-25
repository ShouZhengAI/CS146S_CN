import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal

CHECKBOX_RE = re.compile(r"^\s*[-*]?\s*\[([ xX])\]\s*(.+)$")
PREFIX_RE = re.compile(r"^(?:TODO|ACTION)\s*:\s*", re.IGNORECASE)
PRIORITY_RE = re.compile(r"(?<!\w)@(high|low)\b", re.IGNORECASE)
MENTION_RE = re.compile(r"(?<!\w)@([A-Za-z][\w-]*)")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z][\w-]*)")
ISO_DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
SLASH_DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b")
ACTION_VERBS = {
    "assign",
    "call",
    "complete",
    "email",
    "finish",
    "fix",
    "follow",
    "meet",
    "prepare",
    "review",
    "schedule",
    "send",
    "ship",
    "submit",
    "update",
    "write",
}
WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


@dataclass(frozen=True)
class ExtractedActionItem:
    description: str
    completed: bool
    deadline: str | None
    priority: Literal["high", "normal", "low"]
    assignee: str | None
    tags: tuple[str, ...]


def _deadline(text: str, today: date) -> str | None:
    iso_match = ISO_DATE_RE.search(text)
    if iso_match:
        try:
            return date.fromisoformat(iso_match.group(1)).isoformat()
        except ValueError:
            pass

    slash_match = SLASH_DATE_RE.search(text)
    if slash_match:
        month, day, year = map(int, slash_match.groups())
        try:
            return date(year, month, day).isoformat()
        except ValueError:
            pass

    normalized = text.lower()
    if re.search(r"\b(today|tonight)\b", normalized):
        return today.isoformat()
    if re.search(r"\btomorrow\b", normalized):
        return (today + timedelta(days=1)).isoformat()
    if re.search(r"\bnext week\b", normalized):
        return (today + timedelta(days=7)).isoformat()
    weekday_match = re.search(
        r"\b(?:by|before|on)\s+(" + "|".join(WEEKDAYS) + r")\b",
        normalized,
    )
    if weekday_match:
        target = WEEKDAYS[weekday_match.group(1)]
        days_ahead = (target - today.weekday()) % 7
        return (today + timedelta(days=days_ahead)).isoformat()
    return None


def extract_action_item_details(
    text: str, *, today: date | None = None
) -> list[ExtractedActionItem]:
    reference_date = today or date.today()
    results: list[ExtractedActionItem] = []
    for source_line in text.splitlines():
        line = source_line.strip()
        if not line:
            continue

        checkbox = CHECKBOX_RE.match(line)
        completed = False
        if checkbox:
            completed = checkbox.group(1).lower() == "x"
            description = checkbox.group(2).strip()
        else:
            description = re.sub(r"^\s*[-*]\s+", "", line).strip()

        normalized = description.lower()
        first_word = re.sub(r"[^a-z]", "", normalized.split(maxsplit=1)[0])
        has_marker = PREFIX_RE.match(description) is not None
        has_metadata = bool(
            PRIORITY_RE.search(description)
            or MENTION_RE.search(description)
            or TAG_RE.search(description)
            or _deadline(description, reference_date)
        )
        is_action = bool(
            checkbox
            or has_marker
            or description.endswith("!")
            or first_word in ACTION_VERBS
            or has_metadata
        )
        if not is_action:
            continue

        priority_match = PRIORITY_RE.search(description)
        priority: Literal["high", "normal", "low"] = (
            priority_match.group(1).lower() if priority_match else "normal"
        )
        mentions = [
            match.group(1)
            for match in MENTION_RE.finditer(description)
            if match.group(1).lower() not in {"high", "low"}
        ]
        tags = tuple(dict.fromkeys(match.group(1) for match in TAG_RE.finditer(description)))
        results.append(
            ExtractedActionItem(
                description=description,
                completed=completed,
                deadline=_deadline(description, reference_date),
                priority=priority,
                assignee=mentions[0] if mentions else None,
                tags=tags,
            )
        )
    return results


def extract_action_items(text: str) -> list[str]:
    """Return descriptions for callers using the original Week 7 API."""
    return [item.description for item in extract_action_item_details(text)]



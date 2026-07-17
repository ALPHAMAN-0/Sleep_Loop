"""String utilities. `slugify` is broken on purpose so the loop can heal it."""


def slugify(text: str) -> str:
    # BUG: only lowercases and swaps spaces. Misses punctuation, underscores,
    # hyphen collapsing, and trimming. The loop will fix this.
    return text.lower().replace(" ", "-")

def clean(text):
    if isinstance(text, tuple):
        text = text[1] if len(text) > 1 else ""
    if not isinstance(text, str):
        return ""
    text = text.strip().replace("\u2026", "...").replace("\xa0", " ").replace("\n", " ")
    junk_phrases = [
        "no match", "not found", "404", "error", "none", "no page",
        "no useful information", "No significant", "No relevant", "No description"
    ]
    for junk in junk_phrases:
        if junk in text.lower():
            return ""
    return text

def generate_reason(entity, *notes):
    cleaned = []
    for note in notes:
        c = clean(note)
        if c:
            cleaned.append(c)
    if not cleaned:
        return f"{entity} has no major references or news."
    # Combine to produce a single statement
    return f"{entity}: " + ". ".join(cleaned) + "."

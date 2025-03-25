def generate_reason(entity, wikidata, ofac_note, sec_note, os_note,
                    sentiment_summary, ddg_note, clearbit_note, wayback_note, wiki_note):
    notes = []

    def clean(text):
        if not text:
            return ""
        # Normalize artifacts
        text = text.strip().replace("\u2026", "...").replace("\xa0", " ").replace("\n", " ")

        # Remove junk or default error messages
        blacklist = [
            "no match", "not found", "error", "404", "not available", 
            "no page found", "no mention", "none", "no useful information"
        ]
        if any(bad in text.lower() for bad in blacklist):
            return ""
        return text

    # Clean each note
    for note in [sentiment_summary, wikidata, wiki_note, ddg_note, clearbit_note, wayback_note, sec_note, ofac_note, os_note]:
        cleaned = clean(note)
        if cleaned:
            notes.append(cleaned)

    # Final human-friendly reason
    if not notes:
        return f"{entity} has limited public information available from current sources."

    reason = " ".join(notes)
    reason = reason.replace("..", ".").replace(". .", ".").strip()
    return reason if reason.endswith('.') else reason + "."

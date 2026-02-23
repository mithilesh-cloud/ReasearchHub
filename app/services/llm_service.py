
def generate_answer(question: str, context: str | None = None) -> str:
    context_part = f"\nContext: {context}" if context else ""
    return f"This is a placeholder answer for: {question}{context_part}".strip()

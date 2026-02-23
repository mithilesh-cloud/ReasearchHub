from groq import Groq

from app.core.config import get_settings

settings = get_settings()
client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None


def ask_llm(prompt: str) -> str:
    if not client:
        return (
            "Groq API key is not configured. Here is a context-grounded fallback: \n"
            "- Review the referenced papers for detailed claims.\n"
            "- Use this answer as a draft and verify against full text."
        )

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        temperature=settings.GROQ_TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a precise scientific research assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or "No response generated."

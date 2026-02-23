from hashlib import sha256


def embed_text(text: str, dimensions: int = 8) -> list[float]:
    digest = sha256(text.encode("utf-8")).digest()
    values = [byte / 255 for byte in digest[:dimensions]]
    return values

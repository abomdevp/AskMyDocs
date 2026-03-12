import hashlib


def generate_chunk_id(source: str, chunk_index: int, content: str) -> str:
    raw = f"{source}|{chunk_index}|{content}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()
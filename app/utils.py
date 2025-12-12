import re
import uuid


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or str(uuid.uuid4())


def generate_id() -> str:
    return uuid.uuid4().hex



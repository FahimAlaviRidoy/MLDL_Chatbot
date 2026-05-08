import hashlib


def generate_hash(content: bytes):
    """
    Generate SHA256 hash for duplicate checking.
    """
    return hashlib.sha256(content).hexdigest()
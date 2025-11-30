import re


def chunk_text(text, max_chars=1000, overlap=200):
"""
Breaks long text into smaller overlapping blocks.
"""
text = re.sub(r"\s+", " ", str(text)).strip()
chunks = []
start = 0

while start < len(text):
end = min(start + max_chars, len(text))
block = text[start:end].strip()
chunks.append(block)
start = end - overlap
if start < 0:
start = 0

return chunks

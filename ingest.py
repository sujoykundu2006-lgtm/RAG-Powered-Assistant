from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag import collection, create_embedding

KNOWLEDGE = ROOT / "knowledge"

def chunk_markdown(text: str, source: str):
    sections = re.split(r"(?m)^(?=##? )", text.strip())
    chunks = []

    for index, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue

        chunks.append({
            "id": f"{Path(source).stem}-{index}",
            "text": section,
            "source": source,
        })

    return chunks

def main():
    collection.delete(where={})

    chunks = []

    for path in sorted(KNOWLEDGE.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks.extend(chunk_markdown(text, path.name))

    if not chunks:
        raise RuntimeError("No knowledge files found.")

    for chunk in chunks:
        collection.upsert(
            ids=[chunk["id"]],
            documents=[chunk["text"]],
            embeddings=[create_embedding(chunk["text"])],
            metadatas=[{"source": chunk["source"]}],
        )
        print(f"Indexed {chunk['id']}")

    print(f"\nDone. Indexed {len(chunks)} chunks.")

if __name__ == "__main__":
    main()

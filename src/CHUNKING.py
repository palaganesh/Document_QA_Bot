import pymupdf
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def create_chunks(text):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + CHUNK_SIZE

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


all_chunks = []

for filename in DATA_FOLDER.iterdir():

    if filename.suffix.lower() == ".pdf":

        pdf = pymupdf.open(filename)

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text()

            chunks = create_chunks(text)

            for chunk in chunks:

                all_chunks.append({
                    "text": chunk,
                    "source": filename.name,
                    "page": page_number
                })

        pdf.close()


print("================================")
print("       CHUNKING COMPLETED")
print("================================")

print("Total chunks:", len(all_chunks))

for i, chunk in enumerate(all_chunks[:5], start=1):

    print("\nChunk:", i)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"][:200])
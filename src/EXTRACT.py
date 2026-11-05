import pymupdf
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

print("========================================")
print("       PDF DOCUMENT VERIFICATION")
print("========================================")

for filename in DATA_FOLDER.iterdir():

    if filename.suffix.lower() == ".pdf":

        pdf = pymupdf.open(filename)

        total_words = 0
        empty_pages = 0

        for page in pdf:

            text = page.get_text()
            words = text.split()

            total_words += len(words)

            if not text.strip():
                empty_pages += 1

        total_pages = len(pdf)

        print("\nPDF:", filename.name)
        print("Pages:", total_pages)
        print("Total Words:", total_words)

        if total_pages >= 2 or total_words >= 500:
            print("Status: PASS")
        else:
            print("Status: FAIL")

        if empty_pages > 0:
            print("Empty Pages:", empty_pages)

        pdf.close()

print("\n========================================")
print("       VERIFICATION COMPLETED")
print("========================================")
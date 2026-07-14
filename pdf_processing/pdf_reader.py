from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text(pdf_path):
    """
    Reads a PDF file and returns all its text as a single string.
    """

    try:
        reader = PdfReader(pdf_path)

        all_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                all_text += text + "\n"

        return all_text

    except FileNotFoundError:
        print("Error: PDF file not found.")
        return ""

    except PdfReadError:
        print("Error: Invalid or corrupted PDF.")
        return ""

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return ""
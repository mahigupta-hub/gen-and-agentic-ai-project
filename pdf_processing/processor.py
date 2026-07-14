from pdf_processing.pdf_reader import extract_text
from pdf_processing.text_splitter import split_text


def process_pdf(pdf_path):
    """
    Reads a PDF and returns its text chunks.
    """

    text = extract_text(pdf_path)

    if not text:
        return []

    chunks = split_text(text)

    return chunks
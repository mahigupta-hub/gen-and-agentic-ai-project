from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text):
    """
    Splits text into smaller chunks for RAG.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_text(text)

    return chunks
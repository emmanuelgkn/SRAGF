from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def clean_text(text):
    """
    Fonction permettant de nettoyer un texte
    mal formatté.
    """
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text

def load_pdf(name_file):
    """
    Fonction permettant de charger un ficher pdf
    en afin de le transformer en texte, le nettoyer et
    le découpé en petits morceaux 'chunks' pour le rendre
    ingérable par le modèle.
    """
    loader = PDFPlumberLoader(name_file)

    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150,separators=["\n\n", "\n", ".", " ", ""])
    chunks = text_splitter.split_documents(docs)

    return chunks



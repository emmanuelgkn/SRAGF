from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from lire_pdf import *

def creation_base(chunks):
    """
    Fonction permettant de crée une base d'embeddings 
    correpondants aux chunks données en entrée servant 
    à touver rapidement un paragraphe pertinent à une 
    certaine question dans un texte.
    """
    nom_modele = "dangvantuan/sentence-camembert-large"
    embeddings = HuggingFaceEmbeddings(model_name=nom_modele)



    la_base = Chroma.from_documents(documents=chunks,
                                    embedding=embeddings,
                                    )

    return la_base


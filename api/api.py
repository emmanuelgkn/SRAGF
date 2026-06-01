from fastapi import FastAPI
from pydantic import BaseModel
from main import *

app = FastAPI()

class RequeteDocument(BaseModel):
    chemin : str

class RequeteRAG(BaseModel):
    chemin: str
    question: str

class RequeteLibre(BaseModel):
    question: str

class RequeteComparaison(BaseModel):
    chemin_a: str
    chemin_b: str

class RequeteChatPlusieurs(BaseModel):
    chemin_a: str
    chemin_b: str
    question: str

@app.post("/demander")
def appeler_generation(requette: RequeteRAG):
    reponse = generation_rep(requette.chemin, requette.question)
    
    return {"reponse": reponse}

@app.post("/synthese")
def appeler_synthese(req : RequeteDocument):
    reponse_json = generation_synthese(req.chemin)
    return reponse_json

@app.post("/demander_libre")
def appeler_generation_libre(requete: RequeteLibre):
    reponse = generation_libre(requete.question)
    return {"reponse": reponse}

@app.post("/comparer")
def comaprer_les_fichiers(requete: RequeteComparaison):
    jsona = generation_synthese(requete.chemin_a)
    jsonb = generation_synthese(requete.chemin_b)

    texte_synthese = generation_comparaison(jsona,jsonb)

    return {"doc_a":jsona,"doc_b":jsonb,"texte_synthese":texte_synthese}

@app.post("/demander_plusieurs")
def appeler_generation_multidoc(requete:RequeteChatPlusieurs):
    reponse = generation_multidoc(requete.chemin_a, requete.chemin_b, requete.question)
    return {"reponse": reponse}

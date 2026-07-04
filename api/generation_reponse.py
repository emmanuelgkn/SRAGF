from creation_base_emb import *
import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import numpy as np
import re
import json

def generation_rep(chemin,question,local=True):
    """
    Fonction permettant de générer la réponse à une quesiton 
    concernant un fichier pdf après l'avoir parcouru et récupéré
    les paragraphes pertinents tout en citant ses sources.
    """
    chunks = load_pdf(chemin)
    la_base = creation_base(chunks)
    resultats = la_base.similarity_search(question,k=6)
    res_text = "\n\n".join([doc.page_content for doc in resultats])
    sources = [doc.metadata['page'] for doc in resultats] 

    if local:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")                                                                             
        model = ChatOllama(model="qwen2.5", base_url=base_url)

    else:
        llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-72B-Instruct", 
                                  temperature=0.1,
                                  )
        model = ChatHuggingFace(llm=llm)


    PROMPT = f"""
    RÈGLE ABSOLUE : TU ES UN ASSISTANT FRANCOPHONE. TU DOIS RÉPONDRE UNIQUEMENT EN FRANÇAIS. 
    NE PARLE SOUS AUCUN PRÉTEXTE EN ANGLAIS.
    

    Réponds à la question en te basant uniquement sur le contexte suivant:{res_text}
    Réponds à la question en te basant sur le contexte ci-dessus: {question}.
    Fournis une réponse détaillée.
    Ne justifie pas tes réponses.
    Ne donne pas d’informations qui ne sont pas mentionnées dans le contexte.
    N’utilise pas d’expressions telles que «d’après le contexte», 
    «mentionné dans le contexte» ou toute autre formulation similaire.

    """ 

    response = model.invoke([HumanMessage(content=PROMPT)])
  
    # print("="*50)
    # for line in response.content.split(". "):
    #     print(line.strip())
    # print("="*50,"\n")

    return f"{response.content}\n\n**Pages sources :** {list(np.unique(sources))}"


def generation_synthese(chemin,local=True):
    """
    Fonction permettant de rédiger la synthèse d'un rapport financier 
    en montrant les principaux chiffres le concernant.
    """
    chunks = load_pdf(chemin)
    la_base = creation_base(chunks)
    question = "chiffre d'affaire, resultat net, dette, risques principaux"
    resultats = la_base.similarity_search(question,k=10)
    res_text = "\n\n".join([doc.page_content for doc in resultats])
    # sources = [doc.metadata['page'] for doc, _score in resultats] 

    if local:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")                                                                             
        model = ChatOllama(model="qwen2.5", base_url=base_url)

    else:
        llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-72B-Instruct", 
                                  temperature=0.1,
                                  )
        model = ChatHuggingFace(llm=llm)

    PROMPT = f"""
        RÈGLE ABSOLUE : TU ES UN ASSISTANT FRANCOPHONE. TU DOIS RÉPONDRE UNIQUEMENT EN FRANÇAIS. 
        NE PARLE SOUS AUCUN PRÉTEXTE EN ANGLAIS.

        Règle: Tous les indicateurs financiers (revenue, net_income, debt) doivent être extraits 
        sous forme de montants absolus avec leur devise (ex: 15 milliards d'euros). Convertis tous les 
        montants pour les exprimer uniformément en milliards d'euros (Mds €). Ne donne JAMAIS 
        de pourcentages pour ces champs et toutes les valeurs doivent être positives.

        

        Tu es un extracteur de données financières.
        Analyse le contexte suivant :
        {res_text}

        RÈGLES ABSOLUES :
        1. Tu dois répondre UNIQUEMENT avec un objet JSON valide.
        2. N'ajoute AUCUN texte, bonjour, ou explication avant ou après le JSON.
        3. Utilise exactement et uniquement ces clés en anglais : "revenue", "net_income", "debt", "main_risks".
        4. La clé "main_risks" doit être une liste (array) de chaînes de caractères.
        5. Si une information n'est pas dans le texte, mets "Non renseigné".
        """
    # print(PROMPT)

    response = model.invoke([HumanMessage(content=PROMPT)])

    texte_ia = re.sub(r"^```json\s*", "", response.content.strip(), flags=re.IGNORECASE)
    texte_ia = re.sub(r"\s*```$", "", texte_ia)

    try:
        synthese_dict = json.loads(texte_ia)
        return synthese_dict
        
    except json.JSONDecodeError:
        print("Erreur de parsing JSON. Texte brut renvoyé par l'IA :\n", texte_ia)
        return {
            "revenue": "Erreur d'extraction",
            "net_income": "Erreur d'extraction",
            "debt": "Erreur d'extraction",
            "main_risks": ["Impossible de formater la réponse de l'IA."]
        }


def formateur_formules_math(text):
    """
    Fonction permettant d'adapter la sortie du model pour 
    afficher correctement des formules s'il y en a.
    """
    if not text:
        return text
        
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
    
    def replace_brackets(match):
        content = match.group(1)
        if any(char in content for char in ['=', '\\', '_', '^']):
            return f'$${content}$$'
        return match.group(0)
        
    text = re.sub(r'\[(.*?)\](?!\()', replace_brackets, text, flags=re.DOTALL)
    
    return text

def generation_libre(t,local=True):
    """
    Fonction permettant d'afficher la réponse du model 
    à une question donnée en entrée après avoir traité
    le format (s'il y a des formules mathématiques).
    """
    if local:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")                                                                             
        model = ChatOllama(model="qwen2.5", base_url=base_url)

    else:
        llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-72B-Instruct", 
                                  temperature=0.1,
                                  )
        model = ChatHuggingFace(llm=llm)

    PROMPT = f"""
        {t}
        """

    response = model.invoke([HumanMessage(content=PROMPT)])

    # print("="*50)
    # print(response.content)
    # print("="*50)
    # print(formateur_formules_math(response.content))
    # print("="*50)


    return f"{formateur_formules_math(response.content)}"
 
def generation_comparaison(jsona, jsonb, local=True):
    """
    Fonction permettant de retourner un petit résumé de la comparaison 
    de deux rapports financiers de la même banque sur deux années différentes.
    """

    PROMPT = f"""
        Tu est un analyste financier senior compare ces deux exercices financiers:
        année N-1:{jsona}
        année N:{jsonb}

        Rédige un seul paragraphe en français (max 4 phrases) qui résume l'évolution 
        de l'entreprise (hausse/baisse du CA, de la dette, etc.)
        Sois factuel, précis et professionnel.
        """
    
    if local:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")                                                                             
        model = ChatOllama(model="qwen2.5", base_url=base_url)

    else:
        llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-72B-Instruct", 
                                  temperature=0.1,
                                  )
        model = ChatHuggingFace(llm=llm)

    response = model.invoke([("human", PROMPT)])
    return response.content

def generation_multidoc(chemin_a, chemin_b, question,local=True):
    """
    Fonction permettant de générer la réponse du modele concernant
    deux rapports financiers (de la même banque sur deux années différentes)
    en citant ses sources.
    """
    base_a = creation_base(load_pdf(chemin_a))
    docs_a = base_a.similarity_search(question,k=5)
    contexte_a = "\n".join([d.page_content for d in docs_a])
    sources_a = [d.metadata['page'] for d in docs_a] 

    base_b = creation_base(load_pdf(chemin_b))
    docs_b = base_b.similarity_search(question,k=5)
    contexte_b = "\n".join([d.page_content for d in docs_b])
    sources_b = [d.metadata['page'] for d in docs_b] 

    PROMPT =f"""
        Tu est un analyste financier. Réponds à la question de l'utilisateur en croisant les informations de 
        l'année N-1 et de l'année N.

        CONTEXTE ANNEE N-1:
        {contexte_a}

        CONTEXTE ANNEE N:
        {contexte_b}

        Question:
        {question}
    """

    if local:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")                                                                             
        model = ChatOllama(model="qwen2.5", base_url=base_url)

    else:
        llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-72B-Instruct", 
                                  temperature=0.1,
                                  )
        model = ChatHuggingFace(llm=llm)

    reponse = model.invoke([HumanMessage(content=PROMPT)])

    return f"{reponse.content}\n\n**Sources 1:** {list(np.unique(sources_a))}\n**Sources 2:** {list(np.unique(sources_b))}"

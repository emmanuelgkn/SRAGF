import streamlit as st
import requests
import os 

API = os.getenv("API_URL", "http://localhost:8000")
API_CHAT = f"{API}/demander"
API_SYNTHESE = f"{API}/synthese"

st.set_page_config(page_title="Analyse 1", page_icon="📈")
st.title("📈 Analyser un rapport")
st.markdown("Veuillez choisir un document et lancer l'analyse pour afficher le chat !")

if "synthese" not in st.session_state:
    st.session_state.synthese = None

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    chemin_doc = st.selectbox("Choisissez un rapport :", ["rapports_fin_pdf/rapport_socgen_2025.pdf", 
                                                          "rapports_fin_pdf/rapport_lvmh_2025.pdf",
                                                          "rapports_fin_pdf/rapport_socgen_2024.pdf"])

    if st.button("Analyser ce document"):
        st.session_state.messages = []

        with st.spinner("Génération de la sythèse..."):
            try:
                reponse = requests.post(API_SYNTHESE,json={"chemin":chemin_doc})
                if reponse.status_code == 200:
                    st.session_state.synthese = reponse.json()
                else:
                    st.error(f"Erreur API: {reponse.status_code} - {reponse.text}")
            except requests.exceptions.ConnectionError:
                st.error("Impossible de contacter l'API. Vérifie que le conteneur API tourne.")
if st.session_state.synthese:
    st.subheader("Synthese rapide du rapport")
    data = st.session_state.synthese

    tableau_data = {
        "indicateur":["chiffre d'affaires","Resultat net","Dette totale"],
        "valeur":[data['revenue'], data['net_income'],data['debt']]
    }
    st.table(tableau_data)

    st.markdown("**Risques** : "+", ".join(data['main_risks']))
    st.divider()


if st.session_state.synthese:

    st.markdown("Posez une question sur le rapport financier selectionné")


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: Quel est le chiffre d'affaires 2024 ?"):
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les documents..."):
                try:
                    payload = {
                                "chemin": chemin_doc,
                                "question": prompt
                            }
                    response = requests.post(API_CHAT, json=payload)
                    
                    if response.status_code == 200:
                        reponse_api = response.json().get("reponse","Erreur de format de réponse")
                        st.markdown(reponse_api)
                        
                        st.session_state.messages.append({"role": "assistant", "content": reponse_api})
                    else:
                        st.error(f"Erreur API: {response.status_code} - {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("Impossible de contacter l'API.")

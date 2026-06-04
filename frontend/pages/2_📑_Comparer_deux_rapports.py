import streamlit as st
import requests
import pandas as pd
import os 

API = os.getenv("API_URL", "http://localhost:8000")
API_CHAT = f"{API}/demander_plusieurs"
API_COMPARE = f"{API}/comparer"

st.set_page_config(page_title="Analyse 2", page_icon="📑")
st.title("📑 Comparer deux rapports")

if "messages_groupe" not in st.session_state:
    st.session_state.messages_groupe = []

if "synthese_groupe" not in st.session_state:
    st.session_state.synthese_groupe = None

with st.sidebar:
    doc_1 = st.selectbox("Document 1 :", ["rapports_fin_pdf/rapport_socgen_2024.pdf"])
    doc_2 = st.selectbox("Document 2 :", ["rapports_fin_pdf/rapport_socgen_2025.pdf"])

    if st.button("Lancer l'analyse comparative", use_container_width=True):
        with st.spinner("Analyse et comparaison des deux rapports en cours..."):
            
            payload = {"chemin_a": doc_1, "chemin_b": doc_2}
            
            reponse = requests.post(API_COMPARE, json=payload)

            if reponse.status_code == 200:
                st.session_state.synthese_groupe = reponse.json()

if data := st.session_state.synthese_groupe:
    json_a = data["doc_a"]
    json_b = data["doc_b"]
    st.divider()
    st.subheader("📊 Tableau Comparatif")
    
    tableau_compare = {
        "Indicateur": ["Chiffre d'Affaires", "Résultat Net", "Dette Totale"],
        "Année N-1": [json_a.get('revenue'), json_a.get('net_income'), json_a.get('debt')],
        "Année N": [json_b.get('revenue'), json_b.get('net_income'), json_b.get('debt')]
    }
    
    df = pd.DataFrame(tableau_compare)
    st.table(df.set_index("Indicateur"))
    
    st.subheader("Résumé")
    st.info(data["texte_synthese"])
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("**Risques N-1 :** " + ", ".join(json_a.get('main_risks', [])))
    with col_r2:
        st.markdown("**Risques N :** " + ", ".join(json_b.get('main_risks', [])))

if st.session_state.synthese_groupe:

    for message in st.session_state.messages_groupe:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: Compare les chiffres d'affaires"):
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les documents..."):
                try:
                    payload = {
                                "chemin_a": doc_1,
                                "chemin_b": doc_2,
                                "question": prompt
                            }
                    response = requests.post(API_CHAT, json=payload)
                    
                    if response.status_code == 200:
                        reponse_api = response.json().get("reponse","Erreur de format de réponse")
                        st.markdown(reponse_api)
                        
                        st.session_state.messages_groupe.append({"role": "assistant", "content": reponse_api})
                    else:
                        st.error(f"Erreur API: {response.status_code} - {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("Impossible de contacter l'API.")

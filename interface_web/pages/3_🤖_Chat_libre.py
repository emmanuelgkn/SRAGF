import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/demander_libre"

st.set_page_config(page_title="Chat libre", page_icon="🤖")
st.title("🤖 Chat libre")
st.markdown("Ici vous pouvez converser avec le modele librement sur tout les sujets possibles autre que la finance !")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: Donne la formulation du binome de newton"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            try:
                payload = {
                            "question": prompt
                        }
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    reponse_api = response.json().get("reponse","Erreur de format de réponse")
                    st.markdown(reponse_api)
                    
                    st.session_state.messages.append({"role": "assistant", "content": reponse_api})
                else:
                    st.error(f"Erreur API: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("Impossible de contacter l'API.")

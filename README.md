# 📊 RAG pour la Finance

Un outil d'analyse et de comparaison de rapports financiers basé sur l'architecture RAG (Retrieval-Augmented Generation). Ce projet permet d'interagir avec des documents financiers complexes via un modèle de langage (LLM), tout en garantissant la confidentialité des données traitées.

## ✨ Fonctionnalités Principales

* **🔒 Analyse Confidentielle :** Traitement sécurisé des documents et rapports financiers sensibles pour éviter toute fuite de données.
* **📈 Comparaison Annuelle :** Capacité à ingérer deux rapports financiers sur deux années consécutives pour générer une synthèse comparative des évolutions clés.
* **💬 Interface Conversationnelle (Chat) :** Un assistant interactif permettant de poser des questions libres sur les documents analysés.
* **🧮 Rendu des Formules :** Support avancé permettant au LLM d'afficher correctement et lisiblement les formules mathématiques ou financières directement dans le chat.

## 🛠️ Stack Technique


* **Modèle / NLP :** Qwen2.5 7B
* **Orchestration RAG :** Langchain
* **Backend :** Fastapi
* **Interface Utilisateur :** Streamlit


## 💻 Utilisation

1. Lancer l'interface :

```bash
streamlit run interface_web/🏠_Accueil.py

```


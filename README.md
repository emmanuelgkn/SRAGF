# 📊 RAG pour la Finance

Un outil d'analyse et de comparaison de rapports financiers basé sur l'architecture RAG (Retrieval-Augmented Generation). Ce projet permet d'interagir avec des documents financiers complexes via un grand modèle de langage (LLM), tout en garantissant la confidentialité des données traitées.

## ✨ Fonctionnalités Principales

* **🔒 Analyse Confidentielle :** Traitement sécurisé des documents et rapports financiers sensibles pour éviter toute fuite de données.
* **📈 Comparaison Annuelle :** Capacité à ingérer deux rapports financiers sur deux années consécutives pour générer une synthèse comparative des évolutions clés.
* **💬 Interface Conversationnelle (Chat) :** Un assistant interactif permettant de poser des questions libres sur les documents analysés.
* **🧮 Rendu des Formules :** Support avancé permettant au LLM d'afficher correctement et lisiblement les formules mathématiques ou financières directement dans le chat.

## 🛠️ Stack Technique

*(À adapter selon les outils que tu as réellement utilisés)*

* **Modèle / NLP :** [Nom du LLM, ex: Llama 3, Mistral, OpenAI]
* **Orchestration RAG :** [ex: LangChain, LlamaIndex]
* **Traitement des données :** Python, PyTorch, Pandas
* **Interface Utilisateur :** [ex: Streamlit, Gradio] (avec support Markdown/LaTeX pour les formules)

## 🚀 Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/ton-profil/rag-finance.git
cd rag-finance

```

2. Créer un environnement virtuel et l'activer :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

```

3. Installer les dépendances :

```bash
pip install -r requirements.txt

```

## 💻 Utilisation

1. Déposer les rapports financiers (ex: format PDF) dans le répertoire `data/`.
2. Lancer l'interface :

```bash
streamlit run app.py

```

3. Sélectionner l'option "Analyse simple" ou "Comparaison" et commencer à discuter avec l'assistant.

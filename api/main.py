from generation_reponse import *

# Fichier pour tester si tout marche bien dans le terminal
CHEMIN_FICHIER = "rapports_fin_pdf/rapport_socgen_2025.pdf"

if __name__ == "__main__":
    question = str(input(F"\nPose ta question sur '{CHEMIN_FICHIER}' : "))
    print("")
    generation_rep(CHEMIN_FICHIER,question)


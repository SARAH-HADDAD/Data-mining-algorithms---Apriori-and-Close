import pandas as pd

# Charger les données dans une dataframe
df = pd.read_csv("nom_de_votre_fichier.csv")

# Supprimer les lignes qui contiennent une valeur manquante
df = df.dropna(axis=0, how='any')

# Enregistrer le dataframe dans un nouveau fichier
df.to_csv("nom_du_fichier_sans_valeurs_manquantes.csv", index=False)

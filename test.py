import pandas as pd

# Importer le dataset
df = pd.read_csv("mydata.csv")

# Calculer la moyenne de la colonne "Price in USD"
moyenne = df["Price in USD"].mean()

# Afficher la moyenne
print("La moyenne est de :", moyenne)

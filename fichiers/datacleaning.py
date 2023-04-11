import csv

# Ouvrir le fichier CSV
with open('data/jewelry.csv', 'r') as csvfile:

    # Créer un objet pour lire le contenu du fichier CSV
    reader = csv.reader(csvfile)

    # Ouvrir un nouveau fichier pour écrire le contenu sans les 5 premières colonnes
    with open('nouveau_nom_de_fichier.csv', 'w', newline='') as newfile:

        # Créer un objet pour écrire dans le nouveau fichier CSV
        writer = csv.writer(newfile)

        # Parcourir chaque ligne du fichier CSV
        for row in reader:

            # Écrire la ligne sans les 5 premières colonnes dans le nouveau fichier
            writer.writerow(row[5:])

import numpy as np
from itertools import combinations
import csv
from collections import defaultdict

def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            data.append(row)
    return data

data = load_data('test.csv')
print(data)
# Créer un ensemble d'éléments unique
items = sorted(set([item for transaction in data for item in transaction]))

# Créer un dictionnaire avec les éléments comme clés et des vecteurs binaires correspondants
itemset = {}
for item in items:
    itemset[item] = np.array([1 if item in transaction else 0 for transaction in data])

# candidates initiaux
candidates = list(itemset.keys())
candidates = [[c] for c in candidates]

minsup = 0.5
k = 1
rules = {}
while len(candidates) > 0 :
    #print('Generation: ', k)
    #print('candidates:', candidates)
    # calculer le support des candidats
    frequent_itemsets = []
    closures = []
    for candidate in candidates:
        # trouver la fermeture de candidat
        closure = []
        intersection = itemset[candidate[0]]
        for i in range(1, len(candidate)):
            intersection = intersection & itemset[candidate[i]]
        for item in items:
            if(k<2):
                if itemset[item][itemset[candidate[0]] == 1].all():
                    closure.append(item)
            else:
                if itemset[item][intersection == 1].all():
                    closure.append(item)    
        # si la fermeture de candidat != candidat, alors ajouter à la liste des fermetures
        if closure != candidate:
            # remove candidate in closure
            closure= [x for x in closure if x not in candidate]
            rules[tuple(candidate)] = tuple(closure)
            closures.append(closure)


        support = itemset[candidate[0]]
        for i in range(1, len(candidate)):
            support = support & itemset[candidate[i]]
        # trouver la fermeture de candidat

        support = np.sum(support)/len(data)
        if support >= minsup:
            frequent_itemsets.append(candidate)
        #print('candidate:', candidate, 'support:', support,'fermeture:', closure)
        

    # Générer les candidats de taille k + 1 qui ne contiennent pas d'éléments inférieurs
    #print('closures:', closures)
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            # vérifier que les deux itemsets ont k-1 éléments en commun
            if frequent_itemsets[i][: k - 1] == frequent_itemsets[j][: k - 1]:
                # combiner les deux itemsets pour créer un nouveau candidat
                candidate = frequent_itemsets[i] + [frequent_itemsets[j][-1]]
                # vérifier que tous les k-1 itemsets de candidat sont fréquents
                is_valid = True
                for subset in combinations(candidate, k):
                    if list(subset) not in frequent_itemsets :
                        is_valid = False
                        break
                if is_valid and candidate not in closures :
                    candidates.append(candidate)
    k += 1
print('rules:')
for key, value in rules.items():
    print(f"{key} --> {value}")

import numpy as np
from itertools import combinations


data = [['Apple', 'Banana', 'Lemon', 'Kiwi', 'Fig'],
       ['Apple', 'Banana', 'Lemon', 'Kiwi'],
       ['Pear', 'Fig'],
       ['Apple', 'Banana', 'Kiwi', 'Fig'],
       ['Apple', 'Lemon', 'Kiwi']]

# Créer un ensemble d'éléments unique
items = sorted(set([item for transaction in data for item in transaction]))

# Créer un dictionnaire avec les éléments comme clés et des vecteurs binaires correspondants
itemset = {}
for item in items:
    itemset[item] = np.array([1 if item in transaction else 0 for transaction in data])
#print(itemset)
candidates = list(itemset.keys())

# mettre chaque candidat dans une liste imbriquée
for i in range(len(candidates)):
    candidates[i] = [candidates[i]]

#print(candidates)

base = list(itemset.keys())
#minsup = 2/5
minsup = 2
k = 1

# tant que ensemble de candidats est non vide faire
while len(candidates) > 0 and k < 4:
    print('Generation: ', k)
    print('candidates:', candidates)
    # Calculer le support des candidats
    frequent_itemsets = []
    for candidate in candidates:
        support = []
        for i in range(len(candidate)):
            if i == 0:
                support = itemset[candidate[i]]
            else:
                support = support & itemset[candidate[i]]
        #support = np.sum(support)/len(data)
        support = np.sum(support)
        print('candidate:', candidate)
        print('support:', support)
        if support >= minsup:
            #print('remove:', candidate)
            #candidates.remove(candidate)
            frequent_itemsets.append(candidate)
    # Générer les candidats de taille k + 1
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i+1, len(frequent_itemsets)):
            if frequent_itemsets[i][:k-1] == frequent_itemsets[j][:k-1] and frequent_itemsets[i][k-1] < frequent_itemsets[j][k-1]:
                candidate = frequent_itemsets[i] + [frequent_itemsets[j][k-1]]
                if candidate not in frequent_itemsets and candidate not in candidates:
                    candidates.append(candidate)
    k += 1





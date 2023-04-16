import numpy as np
from itertools import combinations

def generate_combinations(candidates, k):
    return list(combinations(candidates, k))

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
minsup = 2/5
k = 1

# tant que ensemble de candidats est non vide faire
while len(candidates) > 0:
    # Calculer le support des candidats
    for candidate in candidates:
        for i in range(len(candidate)):
            if i == 0:
                support = itemset[candidate[i]]
            else:
                support = support & itemset[candidate[i]]
        support = np.sum(support)
        print('candidate:', candidate)
        print('support:', support)

    k += 1
    new_combinations = generate_combinations(base, k)
    new_candidates = []
        
    if candidates != []:
        for c in new_combinations:
            new_candidates.append(list(c))
        print('_'*20)    
        print('new_candidates:', new_candidates)
        print('_'*20)

    candidates = new_candidates





import numpy as np
from itertools import combinations
import csv

def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]
    return data

def CalculateSupport(itemset,candidate ,num_transactions):
    support = itemset[candidate[0]]
    for i in range(1, len(candidate)):
        support = support & itemset[candidate[i]]
    support = np.sum(support)/num_transactions
    return support

data = load_data('test.csv')
#print(data)
# Créer un ensemble d'éléments unique
items = sorted(set([item for transaction in data for item in transaction]))

# Créer un dictionnaire avec les éléments comme clés et des vecteurs binaires correspondants
itemset = {}
for item in items:
    itemset[item] = np.array(
        [1 if item in transaction else 0 for transaction in data])
#print(itemset)

# candidates initiaux
candidates = [[c] for c in itemset.keys()]

minsup = 2/5
k = 1
rules = {}
while len(candidates) > 0:
    # print('Generation: ', k)
    # print('candidates:', candidates)
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
            if (k < 2):
                if itemset[item][itemset[candidate[0]] == 1].all():
                    closure.append(item)
            else:
                if itemset[item][intersection == 1].all():
                    closure.append(item)
        # Calculate the support of the candidate
        support=CalculateSupport(itemset,candidate ,len(data))

        if support >= minsup:
            frequent_itemsets.append(candidate)
        #print('candidate:', candidate, 'support:',support, 'fermeture:', closure)
        
        # si la fermeture de candidat != candidat, alors ajouter à la liste des fermetures
        if closure != candidate and support >= minsup:
            Rclosure = [x for x in closure if x not in candidate]
            rules[tuple(candidate)] = tuple(Rclosure)
            closures.append(closure)

    # Générer les candidats de taille k + 1 qui ne contiennent pas d'éléments inférieurs
    # print('closures:', closures)
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            # vérifier que les deux itemsets ont k-1 éléments en commun
            if frequent_itemsets[i][: k - 1] == frequent_itemsets[j][: k - 1]:
                # combiner les deux itemsets pour créer un nouveau candidat
                candidate = frequent_itemsets[i] + [frequent_itemsets[j][-1]]
                # vérifier que tous les k-1 itemsets de candidat sont fréquents
                is_valid = all(list(subset) in frequent_itemsets for subset in combinations(candidate, k))
                # candidate est valid si il n'est pas un subset de la closure
                for lst in closures:
                    if set(candidate).issubset(set(lst)):
                        is_valid = False
                if (is_valid) and (candidate not in closures)  :
                    candidates.append(candidate)
    k += 1
    print(closures)
# Print the rules    
print('rules:')
for key, value in rules.items():
    print(f"{key} --> {value}")

from collections import defaultdict
import numpy as np
def calculate_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count

def calculate_closure(itemset, K):
    closure = set(itemset)
    i = 0
    while i < len(K):
        if set(K[i]).issubset(closure):
            closure = closure.union(set(K[i]))
            K.pop(i)
        else:
            i += 1
    return closure

def close_algorithm(candidate_itemsets, minsup, transactions):
    frequent_closed_itemsets = set()
    k=1
    #print('Candidate itemsets: ', candidate_itemsets)
    while candidate_itemsets != [] and k <= 3:
        frequent_itemsets = []
        print('Generation: ', k)
        for item in candidate_itemsets:
            print('Item: ',item)
            support = calculate_support(item, transactions)
            print('Support: ', support)
            if support >= minsup:
                frequent_itemsets.append(item)
        
        for i in range(len(frequent_itemsets)-1):
            for j in range(i+1, len(frequent_itemsets)):
                itemset = sorted(set(frequent_itemsets[i]).union(set(frequent_itemsets[j])))
                if len(itemset) > len(frequent_itemsets[0]) and itemset not in candidate_itemsets:
                    candidate_itemsets.append(itemset)
        k=k+1
    print('Frequent itemsets: ', frequent_itemsets)
                    
data = [['A', 'B', 'C', 'E'], ['A', 'B', 'C', 'D', 'E'], ['A', 'B'], ['C', 'E'], ['A', 'C', 'D']]
candidate_itemsets = sorted(set([item for transaction in data for item in transaction]))
# Créer un dictionnaire avec les éléments comme clés et des vecteurs binaires correspondants
itemset = {}
for item in candidate_itemsets:
    itemset[item] = np.array([1 if item in transaction else 0 for transaction in data])
#print(itemset)
candidates = list(itemset.keys())
minsup = 2

frequent_closed_itemsets = close_algorithm(candidate_itemsets, minsup, data)

print(frequent_closed_itemsets)

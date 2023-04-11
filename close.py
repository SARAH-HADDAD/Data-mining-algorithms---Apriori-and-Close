def get_support(itemset, transactions):
    """
    Fonction qui calcule le support d'un itemset donné dans une liste de transactions.
    """
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count

def get_closure(itemset, transactions):
    """
    Fonction qui calcule la fermeture d'un itemset donné dans une liste de transactions.
    """
    closure = set(itemset)
    old_closure = set()
    while not closure == old_closure:
        old_closure = set(closure)
        for transaction in transactions:
            if set(itemset).issubset(set(transaction)):
                closure.update(set(transaction))
    return closure

def is_closed(itemset, closure, supports):
    """
    Fonction qui vérifie si un itemset donné est fermé en se basant sur sa fermeture et les supports des autres itemsets.
    """
    for element in closure:
        if element != itemset and set(itemset).issubset(set(element)) and supports[itemset] == supports[element]:
            return False
    return True

def get_frequent_closed_itemsets(transactions, minsup):
    """
    Fonction qui retourne l'ensemble des itemsets fermés fréquents dans une liste de transactions donnée, avec un seuil de support minimum.
    """
    itemsets = [frozenset([item]) for transaction in transactions for item in transaction]
    supports = {itemset: get_support(itemset, transactions) for itemset in itemsets}
    closed_itemsets = []
    while itemsets:
        frequent_itemsets = [itemset for itemset in itemsets if supports[itemset] >= minsup]
        for itemset in frequent_itemsets:
            closure = get_closure(itemset, transactions)
            if is_closed(itemset, closure, supports):
                closed_itemsets.append((itemset, closure, supports[itemset]))
        itemsets = [frozenset(set(itemset1) | set(itemset2)) for itemset1 in frequent_itemsets for itemset2 in frequent_itemsets if len(itemset1.union(itemset2)) == len(itemset1) + 1]
        supports = {itemset: get_support(itemset, transactions) for itemset in itemsets}
    return closed_itemsets

data= [['A', 'B', 'C', 'D', 'E'],
       ['A', 'B'],
       ['C', 'E'],
       ['A', 'B', 'D', 'E'],
       ['A' , 'C', 'D' ]]
#On recupere les candidates :
candidates = list(data.keys())
# Set the minimum support 
min_support = 0.1
# Find the closed frequent itemsets
closed_frequent_itemsets = get_frequent_closed_itemsets(data, min_support)
# Print the closed frequent itemsets
print('Closed frequent itemsets:')
for itemset, closure, support in closed_frequent_itemsets:
    print('{}: {} (support: {})'.format(itemset, closure, support))

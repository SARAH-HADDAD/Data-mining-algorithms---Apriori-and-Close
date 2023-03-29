# This function loads the transactional data from a CSV file and converts each transaction into a set of items:
from itertools import combinations
def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            transaction = line.strip().split(',')
            data.append(set(transaction))
    return data
# This function counts the number of times each item appears in the dataset:
def get_item_counts(data):
    item_counts = {}
    for transaction in data:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
    return item_counts
# This function generates all frequent itemsets in the dataset that have a support greater than or equal to the specified minimum support:
def get_frequent_itemsets(data, min_support):
    item_counts = get_item_counts(data)
    num_transactions = len(data)
    min_support_count = num_transactions * min_support
    frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]
    # within each loop iteration, it generates all possible combinations of itemsets of size k
    k = 2
    while frequent_itemsets:
        itemsets = set()
        for i, itemset1 in enumerate(frequent_itemsets):
            for itemset2 in frequent_itemsets[i+1:]:
                new_itemset = itemset1.union(itemset2)
                if len(new_itemset) == k:
                    itemsets.add(new_itemset)
        frequent_itemsets_k = set()
        for itemset in itemsets:
            itemset_count = sum(1 for transaction in data if itemset.issubset(transaction))
            if itemset_count >= min_support_count:
                frequent_itemsets_k.add(itemset)
        if not frequent_itemsets_k:
            break
        frequent_itemsets.extend(frequent_itemsets_k)
        k += 1
        # The loop continues until there are no more frequent itemsets left to generate. 
        # print('the list of frequent itemsets is: ', frequent_itemsets)
    return frequent_itemsets
# This function generates all association rules with a confidence greater than or equal to the specified minimum confidence:
def get_association_rules(frequent_itemsets, min_confidence, data):
    num_transactions = len(data)
    association_rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                antecedent_support = sum(1 for transaction in data if antecedent.issubset(transaction)) / num_transactions
                itemset_support = sum(1 for transaction in data if itemset.issubset(transaction)) / num_transactions
                confidence = itemset_support / antecedent_support
                if confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, confidence))
    return association_rules

# Load the data
data = load_data('insurance.csv')

# Set the minimum support and confidence
#min_support = 0.2

#cela signifie que seules les règles d'association ayant une corrélation de xx0% ou plus seront acceptées.
# Liste des valeurs de min_confidence à tester
min_confidence_range = [0.5, 0.6, 0.7, 0.8, 0.9]

# Boucle pour tester chaque valeur de min_confidence
for min_confidence in min_confidence_range:
    # 
    min_support = 0.1
    frequent_itemsets = get_frequent_itemsets(data, min_support)
    # Trouver les règles d'association avec la valeur actuelle de min_confidence
    association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
    print(len(get_item_counts(data).items()))
    print(get_item_counts(data).items())
    while (len(frequent_itemsets)>len(get_item_counts(data).items())/2):
        min_support += 0.05
        frequent_itemsets = get_frequent_itemsets(data, min_support)        
        association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
    
    # Imprimer les règles d'association et leur performance
    print(f"Règles d'association pour min_confidence = {min_confidence}:")
    for antecedent, consequent, confidence in association_rules:
        print(f"{set(antecedent)} => {set(consequent)} (support={min_support:.3f}, confidence={confidence:.3f})")
    print("\n\n")

from itertools import combinations
from collections import defaultdict

# Function to calculate weighted support
def calculate_wsp(itemset, transactions, weights):
    total_weight = sum(weights)
    itemset_weight = sum([weights[i] for i, transaction in enumerate(transactions) if set(itemset).issubset(set(transaction))])
    return itemset_weight / total_weight

# Function to calculate significance
def calculate_significance(itemset, transactions, weights, min_wsp, min_significance):
    itemset_wsp = calculate_wsp(itemset, transactions, weights)
    if itemset_wsp < min_wsp:
        return False
    for i in range(len(itemset)):
        subset = itemset[:i] + itemset[i+1:]
        subset_wsp = calculate_wsp(subset, transactions, weights)
        if itemset_wsp / subset_wsp < min_significance:
            return False
    return True

# Apriori algorithm using weighted support and significance
def apriori(transactions, weights, min_wsp, min_significance):
    frequent_itemsets = []
    k = 1
    itemsets = set([item for transaction in transactions for item in transaction])
    while itemsets:
        candidate_itemsets = set(combinations(itemsets, k))
        itemsets = set()
        itemset_counts = defaultdict(int)
        for transaction, weight in zip(transactions, weights):
            for candidate in candidate_itemsets:
                if set(candidate).issubset(set(transaction)):
                    itemset_counts[candidate] += weight
        for itemset in candidate_itemsets:
            if calculate_significance(itemset, transactions, weights, min_wsp, min_significance):
                frequent_itemsets.append(itemset)
                itemsets |= set(itemset)
        k += 1
    return frequent_itemsets
transactions = [['A', 'B', 'C', 'D'], ['B', 'D', 'E'], ['A', 'B', 'C', 'D'], ['A', 'B', 'D', 'E'], ['A', 'B', 'C', 'D', 'E'], ['B', 'C', 'E']]
weights = [1.0375, 1.207, 1.0375, 1.155, 1.13, 1.21]
min_wsp = 0.4
min_significance = 1.5

frequent_itemsets = apriori(transactions, weights, min_wsp, min_significance)
print(frequent_itemsets)

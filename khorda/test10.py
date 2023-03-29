# Import necessary libraries
import pandas as pd
from itertools import chain, combinations
import pdb; pdb.set_trace()


# Load the store dataset
store_data = pd.read_csv('data.csv')

# Convert the dataset to a list of transactions
transactions = []
for i in range(len(store_data)):
    transaction = set(store_data.iloc[i].dropna().values)
    transactions.append(transaction)

import itertools

def apriori_with_importance(transactions, min_sup, min_imp):
    # Get list of unique items in transactions
    items = sorted(set([item for transaction in transactions for item in transaction]))
    
    # Calculate importance factor for each item
    item_imp = {}
    for item in items:
        item_count = sum([1 for transaction in transactions if item in transaction])
        item_imp[item] = item_count / len(transactions)
    
    # Initialize list of frequent itemsets
    freq_sets = []
    
    # Generate frequent itemsets of size 1
    freq_1 = []
    for item in items:
        if item_imp[item] >= min_imp:
            itemset = frozenset([item])
            support = sum([1 for transaction in transactions if itemset.issubset(transaction)]) / len(transactions)
            if support >= min_sup:
                freq_1.append(itemset)
                freq_sets.append((itemset, support))
    
    # Generate frequent itemsets of size k (k > 1)
    k = 2
    while freq_sets[-1][0] != frozenset(items):
        candidates = set([frozenset(x) for x in itertools.combinations(set(chain(*freq_sets[-k:])), k)])
        freq_k = []
        for candidate in candidates:
            imp_product = 1
            for item in candidate:
                imp_product *= item_imp[item]
            support = sum([1 for transaction in transactions if candidate.issubset(transaction)]) / len(transactions)
            if support >= min_sup and imp_product >= min_imp:
                freq_k.append(candidate)
                freq_sets.append((candidate, support))
        k += 1
    
    # Print frequent itemsets
    print("Frequent Itemsets:")
    for itemset, support in freq_sets:
        print("{}, Support: {:.2f}".format(list(itemset), support))
    
    # Get itemsets that meet the minimum support and importance thresholds
    picked_itemsets = [itemset for itemset, support in freq_sets if support >= min_sup and item_imp[max(itemset)] >= min_imp]
    
    # Print picked itemsets
    print("\nPicked Itemsets:")
    for itemset in picked_itemsets:
        print(list(itemset))
    
    # Generate association rules from picked itemsets
    rules = []
    for itemset in picked_itemsets:
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset.difference(antecedent)
                antecedent_support = sum([1 for transaction in transactions if antecedent.issubset(transaction)]) / len(transactions)
                consequent_support = sum([1 for transaction in transactions if consequent.issubset(transaction)]) / len(transactions)
                confidence = support / antecedent_support
                lift = confidence / consequent_support
                if confidence >= 0.5 and lift >= 1:
                    rules.append((antecedent, consequent, confidence, lift))
    
    # Print association rules
    print("\nAssociation Rules:")
    for antecedent, consequent, confidence, lift in rules:
        print("{} => {}: Confidence: {:.2f}, Lift: {:.2f}".format(list(antecedent), list(consequent), confidence, lift))
    
    return freq_sets, picked_itemsets, rules


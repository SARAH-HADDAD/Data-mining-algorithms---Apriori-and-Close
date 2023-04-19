import numpy as np
import pandas as pd
import time


def load_data(filename, item_column):
    for elementt in list(data.columns):
        print(type(elementt))
    df = pd.read_csv(filename)
    # Numerate columns
    columns = df.columns.tolist()
    column_dict = {}
    for i, column in enumerate(columns):
        column_dict[i] = column
    # Choose item weight column
    item_weight_column = column_dict[item_column]
    # Calculate item weights
    item_weights = df.groupby(item_weight_column)['Profit'].mean().to_dict()
    # Create a list of transactions
    transactions = []
    for i, row in df.iterrows():
        items = []
        for column in columns:
            if column != item_weight_column and row[column] == 1:
                items.append((column, item_weights[row[item_weight_column]]))
        transactions.append(items)
    return transactions


# Define functions
def calculate_weighted_support(itemset, transactions, weights):
    """Calculates the weighted support of an itemset"""
    itemset_weight = np.mean([weights[item] for item in itemset])
    itemset_count = sum([1 for transaction in transactions
                         if set(itemset).issubset(transaction)])
    total_weight = sum(weights.values())
    return itemset_weight * itemset_count / total_weight


def generate_frequent_itemsets(transactions, min_support, weights=None):
    """Generates frequent itemsets above a minimum support threshold"""
    items = set([item for transaction in transactions for item in transaction])
    if weights is None:
        weights = {item: 1 for item in items}
    frequent_itemsets = []
    k = 1
    while True:
        itemsets = [frozenset([item]) for item in items if weights[item] >= min_support]
        if not itemsets:
            break
        frequent_itemsets.extend(itemsets)
        while True:
            k += 1
            new_itemsets = []
            for itemset in itemsets:
                for item in items:
                    if item not in itemset:
                        new_itemset = itemset | frozenset([item])
                        if weights[item] >= min_support and \
                                all([subset in frequent_itemsets for subset in new_itemset]):
                            new_itemsets.append(new_itemset)
            if not new_itemsets:
                break
            frequent_itemsets.extend(new_itemsets)
            itemsets = new_itemsets
    return frequent_itemsets


def generate_association_rules(frequent_itemsets, transactions, min_confidence, weights=None):
    """Generates association rules above a minimum confidence threshold"""
    if weights is None:
        weights = {item: 1 for item in set([item for transaction in transactions for item in transaction])}
    association_rules = []
    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            for item in itemset:
                antecedent = itemset - frozenset([item])
                consequent = frozenset([item])
                support = calculate_weighted_support(itemset, transactions, weights)
                confidence = calculate_weighted_support(itemset, transactions, weights) / \
                             calculate_weighted_support(antecedent, transactions, weights)
                if confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, support, confidence))
    return association_rules


start_time = time.time()
# Load data
data = pd.read_csv('Supermart_Grocery_Sales.csv')
# Set minimum support and minimum confidence thresholds
min_support = 0.1
min_confidence = 0.5

# Select the column to use for
print("Column names:", list(data.columns))
column = str(input("Enter the column to use for item weights: "))
transactions, item_weight = load_data('Supermart Grocery Sales.csv', column)
frequent_itemsets = generate_frequent_itemsets(transactions, min_support, item_weight)
association_rules = generate_association_rules(frequent_itemsets, transactions, min_confidence, item_weight)
print("Frequent itemsets:")
for itemset in frequent_itemsets:
    print(list(itemset))

print("\nAssociation rules:")
for antecedent, consequent, support, confidence in association_rules:
    print(list(antecedent), "=>", list(consequent), "(support:", round(support, 2), ", confidence:", round(confidence, 2), ")")
print("\n")
end_time = time.time()
total_time = end_time - start_time
print("Le temps d'exÃ©cution est de : ", total_time, " secondes")
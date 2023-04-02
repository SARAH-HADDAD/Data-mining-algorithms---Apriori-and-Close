from itertools import combinations
# This function loads the transactional data from a CSV file and converts each transaction into a set of items in order:
import csv

def load_data(file_path):
    data = []
    Profit = []  # add this list to store all the "Price in USD" values
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # récupérer la première ligne en tant qu'en-tête
        for row in reader:
            data.append(row)
            Profit.append(float(row[2])) 
    return data, Profit 

# This function counts the number of times each item appears in the dataset and the profit of each item:
def get_item_counts(data):
    item_counts = {}
    for transaction in data:
        # (transaction[2]) c'est le profit
        for i in range(0, len(transaction)):
            if transaction[i] in item_counts:
                item_counts[transaction[i]]["count"] += 1
                # if the profit of the item is greater than the profit of the item in the dictionary, we replace it
                if(transaction[2]>item_counts[transaction[i]]["profit"]):item_counts[transaction[i]]["profit"] = transaction[2]
            else:
                # if the item is not in the dictionary, we add it
                # the profit of the item is the profit of the transaction
                item_counts[transaction[i]] = {"count":1,"profit":transaction[2]}
    print('item_counts:',item_counts)
    return item_counts

# This function generates all frequent itemsets in the dataset that have a support greater than or equal to the specified minimum support:
def get_frequent_itemsets(data, min_support,Profit):
    item_counts = get_item_counts(data)
    #print(item_counts)
    num_transactions = len(data)
    # get the sum of Profit of all items
    sum_Profit = sum(Profit)
    #print('sum_Profit:',sum_Profit)
    min_support_count = num_transactions * min_support  
    min_support_profit = sum_Profit * min_support 
    print('min_support_count:',min_support_count)
    print('min_support_profit:',min_support_profit)
    importantxfrequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if (count["count"] * float(count["profit"])) >= min_support_profit*min_support_count]
    k = 2
    while importantxfrequent_itemsets:
        itemsets = set()
        for i, itemset1 in enumerate(importantxfrequent_itemsets):
            for itemset2 in importantxfrequent_itemsets[i+1:]:
                new_itemset = itemset1.union(itemset2)
                if len(new_itemset) == k:
                    itemsets.add(new_itemset)
        importantxfrequent_itemsets_k = set()
        for itemset in itemsets:
            itemset_count = sum(1 for transaction in data if itemset.issubset(transaction))
            # check if the items have a great profit
            total_profit = sum([item_counts[item]["profit"] for item in itemset])
            if (itemset_count >= min_support_count) or (total_profit >= min_support_profit * itemset_count):
                importantxfrequent_itemsets_k.add(itemset)
        if not importantxfrequent_itemsets_k:
            break
        importantxfrequent_itemsets.extend(importantxfrequent_itemsets_k)
        k += 1

    return importantxfrequent_itemsets

# This function generates all association rules with a confidence greater than or equal to the specified minimum confidence:
def get_association_rules(importantxfrequent_itemsets, min_confidence, data):
    num_transactions = len(data)
    item_counts = get_item_counts(data)
    association_rules = []
    for itemset in importantxfrequent_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                antecedent_support = sum(1 for transaction in data if antecedent.issubset(transaction)) / num_transactions
                itemset_support = sum(1 for transaction in data if itemset.issubset(transaction)) / num_transactions
                confidence = itemset_support / antecedent_support
                # Calculate weighted confidence
                weighted_confidence = confidence * item_counts[consequent]["profit"]
                if weighted_confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, weighted_confidence, item_counts[consequent]["profit"], antecedent_support))
    return association_rules

# Load the data
data, Profit = load_data('test.csv')
# Set the minimum support and confidence
min_support = 0.2
min_confidence = 0.5
print(f"Règles d'association pour min_confidence = {min_confidence}:")
print(f"Règles d'association pour min_support = {min_support}:")
# Find the frequent itemsets
frequent_itemsets = get_frequent_itemsets(data, min_support,Profit)
# Trouver les règles d'association avec la valeur actuelle de min_confidence
association_rules = get_association_rules(frequent_itemsets, min_confidence, data)

# Imprimer les règles d'association et leur performance
for antecedent, consequent, weighted_confidence, profit, support in association_rules:
    print(f"{set(antecedent)} => {set(consequent)} (weighted confidence={weighted_confidence:.3f}, profit={profit:.2f}, support={support:.3f})")
    print("\n\n")

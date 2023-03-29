from itertools import combinations
# This function loads the transactional data from a CSV file and converts each transaction into a set of items in order:
import csv

def load_data(file_path):
    data = []
    prices = []  # add this list to store all the "Price in USD" values
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # récupérer la première ligne en tant qu'en-tête
        for row in reader:
            data.append(row)
            prices.append(float(row[2])) 
    return data, prices 


# This function counts the number of times each item appears in the dataset:
def get_item_counts(data,average_price):
    item_counts = {}
    item_importance = {}
    for transaction in data:
        #print(transaction[2])
        if float(transaction[2]) > average_price:
            importance=1
        else:
            importance=0
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
                item_importance[item] += importance
            else:
                item_counts[item] = 1
                item_importance[item] = importance
    return item_counts,item_importance
# This function generates all frequent itemsets in the dataset that have a support greater than or equal to the specified minimum support:
def get_frequent_itemsets(data, min_support,average_price):
    item_counts,item_importance = get_item_counts(data,average_price)
    #print(item_counts)
    num_transactions = len(data)
    min_support_count = num_transactions * min_support
    frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]
    frequentximportant_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count or item_importance.get(item, 0) >= 1]
    print('frequentximportant_itemsets:',frequentximportant_itemsets)
    print('frequent_itemsets:',frequent_itemsets)
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
data, prices = load_data('test.csv')
average_price = sum(prices) / len(prices)
print(f"The average price in USD is {average_price:.2f}")
# Set the minimum support and confidence
min_support = 0.5
min_confidence = 0.5
print(f"Règles d'association pour min_confidence = {min_confidence}:")
print(f"Règles d'association pour min_support = {min_support}:")
# Find the frequent itemsets
frequent_itemsets = get_frequent_itemsets(data, min_support,average_price)
# Trouver les règles d'association avec la valeur actuelle de min_confidence
association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
# Imprimer les règles d'association et leur performance
for antecedent, consequent, confidence in association_rules:
    print(f"{set(antecedent)} => {set(consequent)} (support={min_support:.3f}, confidence={confidence:.3f})")
    print("\n\n")

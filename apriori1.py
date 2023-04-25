from itertools import combinations
import csv
from collections import defaultdict

def load_data(file_path,column):
    data = []
    Profit = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        for row in reader:
            data.append(row)
            Profit.append(float(row[column])) 
    return data, Profit

# Function to calculate weighted support
def calculate_wsp(itemset, transactions, weights):
    total_weight = sum(weights)
    itemset_weight = sum([weights[i] for i, transaction in enumerate(transactions) if set(itemset).issubset(set(transaction))])
    print(itemset)
    print(itemset_weight / total_weight)
    return itemset_weight / total_weight

def get_item_counts(data):
    item_counts = defaultdict(int) 
    for transaction in data:
        for item in transaction:
            item_counts[item] += 1
    return item_counts

def get_frequent_itemsets(data, min_support):
    item_counts = get_item_counts(data)
    num_transactions = len(data)
    min_support_count = num_transactions * min_support
    frequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if count >= min_support_count]
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
    return frequent_itemsets

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



# Set minimum support and minimum confidence thresholds
min_support = 0.5
min_confidence = 0.5
#min_significance = 0.5
# Load data
data,Profit = load_data('test.csv',3)
# Select the column to use for
#print("Column names:", list(test))
#column = int(input("Enter the column to use for item weights: "))
#print(column)
#print('test')
calculate_wsp(['B', 'D'], data, Profit)
frequent_itemsets = get_frequent_itemsets(data, min_support)
association_rules = get_association_rules(frequent_itemsets, min_confidence,data)
#print("Frequent itemsets:")
#for itemset in frequent_itemsets:
#    print(list(itemset))

print("\nAssociation rules:")
for antecedent, consequent, confidence in association_rules:
    print(list(antecedent), "=>", list(consequent), ", confidence:", round(confidence, 2), ")")
print("\n")

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


# Load the data
data = load_data('data.csv')


num_transactions = len(data)
sorted_item_counts = sorted(get_item_counts(data).items(), key=lambda x: x[1], reverse=True)
cumulative_count = 0
for item, count in sorted_item_counts:
    item_support = count / num_transactions
    cumulative_count += count
    if cumulative_count >= 0.8 * num_transactions:
        min_support = item_support
        break
# Find the frequent itemsets
frequent_itemsets = get_frequent_itemsets(data, min_support)
# Trouver les règles d'association avec la valeur actuelle de min_confidence
while not frequent_itemsets:
    min_support -= 0.05
    #min_support -= 0.1
    frequent_itemsets = get_frequent_itemsets(data, min_support)    

frequent_itemsets = get_frequent_itemsets(data, min_support)
print('the minimum support is: ', min_support)
print('the list of frequent itemsets is: ')
for f in frequent_itemsets:
    print(f)
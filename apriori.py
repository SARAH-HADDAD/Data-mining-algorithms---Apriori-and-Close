from itertools import combinations
import time

def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            transaction = line.strip().split(',')
            data.append(set(transaction))
    return data

def get_item_counts(data):
    item_counts = {}
    for transaction in data:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
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
    # Identify closed frequent itemsets
    closed_frequent_itemsets = []
    for itemset1 in frequent_itemsets:
        is_closed = True
        for itemset2 in frequent_itemsets:
            if itemset1 != itemset2 and itemset1.issubset(itemset2) and itemset1 in item_counts and itemset2 in item_counts and item_counts[itemset1] == item_counts[itemset2]:
                is_closed = False
                break
        if is_closed:
            closed_frequent_itemsets.append(itemset1)
    return closed_frequent_itemsets

def get_association_rules(closed_frequent_itemsets, min_confidence, data):
    num_transactions = len(data)
    association_rules = []
    for itemset in closed_frequent_itemsets:
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

start_time = time.time()
data = load_data('SampleSuperstore.csv')
min_support = 0.2
min_confidence = 0.5
frequent_itemsets = get_frequent_itemsets(data, min_support)
closed_frequent_itemsets = frequent_itemsets  # Only consider closed frequent itemsets
association_rules = get_association_rules(closed_frequent_itemsets,min_confidence, data)

print(f"Found {len(closed_frequent_itemsets)} closed frequent itemsets:")
for itemset in closed_frequent_itemsets:
    print(itemset)

print(f"Found {len(association_rules)} association rules:")
for rule in association_rules:
    print(f"{rule[0]} -> {rule[1]} (confidence: {rule[2]})")

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds.")
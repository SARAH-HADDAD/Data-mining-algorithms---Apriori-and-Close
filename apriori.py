import csv
from itertools import combinations
from collections import defaultdict

def load_data(file_path,column):
    data = []
    Profit = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            data.append(row)
            Profit.append(float(row[column])) 
    return data, Profit

# Function to calculate weighted support
def calculate_wsp(itemset, transactions, weights): #min sup pondere
    total_weight = sum(weights)
    itemset_weight = 0
    for i, transaction in enumerate(transactions):
        if set(itemset).issubset(set(transaction)):
            itemset_weight += weights[i]
        else:
            if(itemset  in transaction ):
                itemset_weight += weights[i]

    return itemset_weight / total_weight

def get_item_weight(data,weights):
    item_weights = defaultdict(int) 
    for transaction in data:
        for item in transaction:
            item_weights[item] =calculate_wsp(item,data,weights) 
    return item_weights

def get_weighted_itemsets(data, min_support,weights):
    item_weights = get_item_weight(data,weights)
    weighted_itemsets = [frozenset({item}) for item, count in item_weights.items() if count >= min_support]
    k = 2
    while weighted_itemsets:
        itemsets = set()
        for i, itemset1 in enumerate(weighted_itemsets):
            for itemset2 in weighted_itemsets[i+1:]:
                new_itemset = itemset1.union(itemset2)
                if len(new_itemset) == k:
                    itemsets.add(new_itemset)
        frequent_itemsets_k = set()
        for itemset in itemsets:
            if  calculate_wsp(itemset,data,weights)>= min_support:
                frequent_itemsets_k.add(itemset)
        if not frequent_itemsets_k:
            break
        weighted_itemsets.extend(frequent_itemsets_k)
        k += 1
    return weighted_itemsets

def get_association_rules(weighted_itemsets, min_confidence, data,weights):
    association_rules = []
    for itemset in weighted_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                antecedent_support = calculate_wsp(antecedent,data,weights)
                itemset_support = calculate_wsp(itemset,data,weights)
                confidence = itemset_support / antecedent_support
                test= antecedent_support/itemset_support 
                if confidence >= min_confidence :
                    association_rules.append((antecedent, consequent, confidence))
    return association_rules

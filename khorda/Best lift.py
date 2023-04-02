
# This function loads the transactional data from a CSV file and converts each transaction into a set of items:
from itertools import combinations
import numpy as np 
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
                consequent_support = sum(1 for transaction in data if consequent.issubset(transaction)) / num_transactions
                itemset_support = sum(1 for transaction in data if itemset.issubset(transaction)) / num_transactions
                confidence = itemset_support / antecedent_support
                lift = confidence / consequent_support
                if confidence >= min_confidence:
                    association_rules.append((antecedent, consequent, confidence, lift))
    return association_rules


def find_best_lift(data):
    min_support = 0.1
    best_lift = None
    best_support = None
    min_confidence = 0.5
    
    while min_support <= 1.0:
        frequent_itemsets = get_frequent_itemsets(data, min_support)
        association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
        lift_value =0

        for antecedent, consequent, confidence,lift in association_rules:
            if(abs(lift)!=1):
                lift_value += abs(lift)
        num_association_rules = len(association_rules)
        if(num_association_rules>0):
            lift_value=lift_value/num_association_rules
        #and lift_value > 1
        if(best_lift is None): best_lift=lift_value
        if(best_support is None): best_support=min_support
        print('min_support',min_support)
        print('lift_value',lift_value)
        print('best_lift',best_lift)
        print('best_support',best_support)
        print('\n')
        if num_association_rules>0 and lift_value > best_lift :
            print("test2")
            best_lift = lift_value
            best_support = min_support
            print("test")
        if(num_association_rules==0 ):
            print(min_support)
            print(best_support)
            break
        min_support += 0.1
    
    if best_support is not None:
        print(f"Best lift: {best_lift:.3f} with min_support={best_support}")
        
        frequent_itemsets = get_frequent_itemsets(data, best_support)
        association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
        
        print(f"Association rules")
        
        for antecedent, consequent, confidence,lift in association_rules:
            print(f"{set(antecedent)} => {set(consequent)} (support={best_support:.3f}, confidence={confidence:.3f}, lift={lift:.3f})")
    else:
        print(f"No association rules found with lift greater than {best_lift}")

#lift(A -> B) = support(A and B) / (support(A) * support(B))


data = load_data('bank-data.csv')
#min_support_range = [0.1, 0.2, 0.3, 0.4, 0.5]
#lift_range = [1.1, 1.2, 1.3, 1.4, 1.5]
#min_support_range = np.arange(0.01, 0.51, 0.01)
find_best_lift(data)







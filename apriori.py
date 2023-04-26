import csv
from itertools import combinations
from collections import defaultdict
def predict_min_weighted_support(data, weights):
    num_transactions=len(data)
    num_items=len(set(item for transaction in data for item in transaction))
    # calculate average weight
    avg_weight = sum(weights) / len(weights)
    
    # calculate skewness of weight distribution
    weight_variance = sum((w - avg_weight) ** 2 for w in weights) / len(weights)
    weight_stddev = weight_variance ** 0.5
    skewness = sum((w - avg_weight) ** 3 for w in weights) / (len(weights) * weight_stddev ** 3)
    
    # predict optimal min_weighted_support
    min_support = 0.05
    if num_transactions > 1000:
        min_support = 0.02
    elif num_transactions > 500:
        min_support = 0.03
    elif num_transactions > 100:
        min_support = 0.04
    
    if num_items > 50:
        min_support += 0.02
    elif num_items > 100:
        min_support += 0.03
    
    if skewness > 1:
        min_support -= 0.01
    
    return min_support

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
    #print(item_weights)    
    return item_weights

def get_weighted_itemsets(data, min_support,weights):
    item_weights = get_item_weight(data,weights)
    weighted_itemsets = [frozenset({item}) for item, count in item_weights.items() if count >= min_support]
    #print('frequent ',weighted_itemsets)
    k = 2
    while weighted_itemsets:
        print(k)
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



# Set minimum support and minimum confidence thresholds
data,Profit = load_data('Supermart_Grocery_Sales.csv',9)
min_support = predict_min_weighted_support(data, Profit)
print('mins_support=',min_support)
min_confidence = 0.5
# Select the column to use for
#print("Column names:", list(test))
#column = int(input("Enter the column to use for item weights: "))
#print(column)
#print('test')
weighted_itemsets = get_weighted_itemsets(data, min_support,Profit)
association_rules = get_association_rules(weighted_itemsets, min_confidence,data,Profit)

print("\nAssociation rules:")
for antecedent, consequent, confidence in association_rules:
    print(list(antecedent), "=>", list(consequent), ", confidence:", round(confidence, 2), ")")
print("\n")

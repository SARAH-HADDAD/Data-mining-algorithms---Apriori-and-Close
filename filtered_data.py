import csv

# This function loads the transactional data from a CSV file and converts each transaction into a set of items in order:

def load_data(file_path):
    data = []
    Profit = []  # add this list to store all the "Price in USD" values
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # récupérer la première ligne en tant qu'en-tête
        for row in reader:
            data.append(row)
            print(row[1])
            Profit.append(float(row[1])) 
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
                if(transaction[1]>item_counts[transaction[i]]["profit"]):item_counts[transaction[i]]["profit"] = transaction[1]
            else:
                # if the item is not in the dictionary, we add it
                # the profit of the item is the profit of the transaction
                item_counts[transaction[i]] = {"count":1,"profit":transaction[1]}
    #print('item_counts:',item_counts)
    return item_counts

def filter_data(data,Profit):
    item_counts = get_item_counts(data)
    num_transactions = len(data)
    sum_Profit = sum(Profit)
    avg_profit = sum_Profit / num_transactions
    print('avrage profit:',avg_profit)
    importantxfrequent_itemsets = [frozenset({item}) for item, count in item_counts.items() if (count["count"] * float(count["profit"])) >= avg_profit]
    print('importantxfrequent_itemsets:',importantxfrequent_itemsets)
    
    filtered_data = []
    for transaction in data:
        if has_itemset(transaction,importantxfrequent_itemsets):
            filtered_data.append(transaction)
    return filtered_data

def has_itemset(transaction, itemsets):
    for itemset in itemsets:
        if set(itemset).issubset(set(transaction)):
            return True
    print('9iw',transaction)
    return False

# Load the data
data, Profit = load_data('test.csv')

# Filter the data
filtered_data = filter_data(data, Profit)

# Write the filtered data to a CSV file
with open('new_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(filtered_data)

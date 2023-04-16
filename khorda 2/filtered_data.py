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
            print(row[2])
            Profit.append(float(row[2])) 
    return data, Profit 

# This function counts the number of times each item appears in the dataset and the profit of each item:
def get_item_counts(data):
    item_counts = {}
    for transaction in data:
        for i in [0, 1, 5]:
            if transaction[i] in item_counts:
                item_counts[transaction[i]]["count"] += 1
                if(transaction[2] > item_counts[transaction[i]]["profit"]):
                    item_counts[transaction[i]]["profit"] = transaction[2]
            else:
                item_counts[transaction[i]] = {"count":1,"profit":transaction[2]}
    return item_counts

def filter_data(data, Profit):
    item_counts = get_item_counts(data)
    num_transactions = len(data)
    sum_Profit = sum(Profit)
    avg_profit = sum_Profit / num_transactions
    importantxfrequent_itemsets = [frozenset({"pendant"}), frozenset({"earring"}), frozenset({"bracelet"}), frozenset({"ring"})]
    
    filtered_data = []
    for transaction in data:
        if has_itemset(transaction,importantxfrequent_itemsets):
            filtered_data.append(transaction)
    return filtered_data

def has_itemset(transaction, itemsets):
    for itemset in itemsets:
        if set(itemset).issubset(set([transaction[i] for i in [0, 1, 2, 4, 5, 6]])):
            return True
    return False

# Load the data
data, Profit = load_data('mydata.csv')

# Filter the data
filtered_data = filter_data(data, Profit)

# Write the filtered data to a CSV file
with open('new_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['Category', 'Brand ID', 'Price in USD', 'User ID', 'Gender', 'Color', 'type'])
    # Write the filtered data
    for row in filtered_data:
        writer.writerow(row)
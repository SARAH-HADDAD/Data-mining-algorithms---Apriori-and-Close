import csv
def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # récupérer la première ligne en tant qu'en-tête
        for row in reader:
            data.append(row)
    return data 
def filter_data(data, importantxfrequent_itemsets):
    filtered_data = []
    for transaction in data:
        if set(transaction).intersection(importantxfrequent_itemsets):
            filtered_data.append(transaction)
    return filtered_data
# Load the data
data = load_data('test.csv')
importantxfrequent_itemsets=['red']
print(len(filter_data(data, importantxfrequent_itemsets)))
import tkinter as tk
from tkinter import filedialog
from apriori import load_data, get_frequent_itemsets, get_association_rules
import csv

# This function loads the transactional data from a CSV file and converts each transaction into a set of items in order:

def load_data(file_path,colonne):
    data = []
    Profit = []  # add this list to store all the "Price in USD" values
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # récupérer la première ligne en tant qu'en-tête
        for row in reader:
            data.append(row)
            print(row[colonne])
            Profit.append(float(row[colonne])) 
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

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Association Rule Mining")
        
        self.file_label = tk.Label(self.master, text="Select CSV file:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.file_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.file_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.min_support_label = tk.Label(self.master, text="Minimum Support:")
        self.min_support_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.min_support_entry = tk.Entry(self.master)
        self.min_support_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.min_confidence_label = tk.Label(self.master, text="Minimum Confidence:")
        self.min_confidence_label.grid(row=2, column=0, padx=10, pady=10)
      
        self.min_confidence_entry = tk.Entry(self.master)
        self.min_confidence_entry.grid(row=2, column=1, padx=10, pady=10)

        self.poid = tk.Label(self.master, text="Poid:")
        self.poid.grid(row=3, column=0, padx=10, pady=10)
        self.poid_entry = tk.Entry(self.master)
        self.poid_entry.grid(row=3, column=1, padx=10, pady=10) 
        
        self.run_button = tk.Button(self.master, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        
    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    def run_algorithm(self):
        try:
            min_support = float(self.min_support_entry.get())
            min_confidence = float(self.min_confidence_entry.get())
            poid = float(self.poid_entry.get())
            # Load the data
            data, Profit = load_data(self.file_path,poid)
            # Filter the data
            filtered_data = filter_data(data, Profit)
            frequent_itemsets = get_frequent_itemsets(filtered_data, min_support)
            association_rules = get_association_rules(frequent_itemsets, min_confidence, data)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Association rules for min_confidence = {min_confidence} and min_support = {min_support}:\n\n")
            for antecedent, consequent, confidence in association_rules:
                self.result_text.insert(tk.END, f"{set(antecedent)} => {set(consequent)} (support={min_support:.3f}, confidence={confidence:.3f})\n\n")
        except Exception as e:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Error: {e}")

root = tk.Tk()
app = App(root)
root.mainloop()

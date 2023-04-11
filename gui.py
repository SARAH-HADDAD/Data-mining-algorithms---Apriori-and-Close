import tkinter as tk
from tkinter import filedialog
from apriori import load_data, get_frequent_itemsets, get_association_rules

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
        
        self.run_button = tk.Button(self.master, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    def run_algorithm(self):
        try:
            data = load_data(self.file_path)
            min_support = float(self.min_support_entry.get())
            min_confidence = float(self.min_confidence_entry.get())
            frequent_itemsets = get_frequent_itemsets(data, min_support)
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

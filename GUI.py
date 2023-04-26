import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from apriori import load_data, get_weighted_itemsets, get_association_rules,get_item_weight
from Close import CloseAlgorithm, Load_data, CalculateSupport
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
class AssociationRulesGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("Association Rules")
        master.geometry("400x220") # set window size

        self.label = tk.Label(master, text="\n Please select the algorithm and dataset file.")
        self.label.pack()

        self.algorithm_var = tk.StringVar(master)
        self.algorithm_var.set("Apriori") # default value

        self.algorithm_menu = tk.OptionMenu(master, self.algorithm_var, "Apriori", "Close")
        self.algorithm_menu.pack()

        self.dataset_path = ""

        self.dataset_button = tk.Button(master, text="Select Dataset", command=self.select_dataset_file)
        self.dataset_button.pack()

        self.apriori_frame = tk.Frame(master)
        self.min_support_label = tk.Label(self.apriori_frame, text="Minimum Support")
        self.min_support_label.pack(side=tk.LEFT)
        self.min_support_entry = tk.Entry(self.apriori_frame)
        self.min_support_entry.pack(side=tk.LEFT)
        self.apriori_frame.pack()

        self.min_confidence_frame = tk.Frame(master)
        self.min_confidence_label = tk.Label(self.min_confidence_frame, text="Minimum Confidence")
        self.min_confidence_label.pack(side=tk.LEFT)
        self.min_confidence_entry = tk.Entry(self.min_confidence_frame)
        self.min_confidence_entry.pack(side=tk.LEFT)
        self.min_confidence_frame.pack()

        self.close_frame = tk.Frame(master)
        self.weight_column_label = tk.Label(self.close_frame, text="Weight Column (0-indexed)")
        self.weight_column_label.pack(side=tk.LEFT)
        self.weight_column_entry = tk.Entry(self.close_frame)
        self.weight_column_entry.pack(side=tk.LEFT)
        self.close_frame.pack()

        self.run_button = tk.Button(master, text="Run", command=self.run_algorithm)
        self.run_button.pack()

    def select_dataset_file(self):
        self.dataset_path = filedialog.askopenfilename(initialdir="./", title="Select dataset file",
                                                       filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        if self.dataset_path:
            messagebox.showinfo("File Selected", f"Dataset file selected:\n{self.dataset_path}")
        else:
            messagebox.showwarning("File Not Selected", "No dataset file selected.")

    def run_algorithm(self):
        algorithm = self.algorithm_var.get()
        if not self.dataset_path:
            messagebox.showwarning("File Not Selected", "No dataset file selected.")
            return
        if algorithm == "Apriori":
            min_support = self.min_support_entry.get()
            if not min_support:
                messagebox.showwarning("Missing Parameter", "Please enter the minimum support value.")
                return
            min_confidence = self.min_confidence_entry.get()
            if not min_confidence:
                messagebox.showwarning("Missing Parameter", "Please enter the minimum confidence value.")            
            weight_column = self.weight_column_entry.get()
            if not weight_column:
                messagebox.showwarning("Missing Parameter", "Please enter the weight column index.")
                return           
            # Load the data from the selected file
            data,weights = load_data(self.dataset_path,int(weight_column))
            weighted_itemsets = get_weighted_itemsets(data,float(min_support),weights)
            item_weight=get_item_weight(data,weights)
            # Plot the pie chart
            figure_window = tk.Toplevel(self.master)
            figure_window.title("items weights")
            labels = list(item_weight.keys())
            sizes = list(item_weight.values())
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')
            # Embed the figure in a Tkinter canvas
            canvas = FigureCanvasTkAgg(fig, master=figure_window)
            canvas.draw()
            canvas.get_tk_widget().pack()
            association_rules = get_association_rules(weighted_itemsets, float(min_confidence),data,weights)
            # Display the association rules in a new window
            rule_window = tk.Toplevel(self.master)
            rule_window.title("Association Rules")
            rule_text = tk.Text(rule_window, wrap=tk.WORD)
            rule_text.pack()
            for antecedent, consequent, confidence in association_rules:
                rule_text.insert(tk.END, f"{set(antecedent)} => {set(consequent)} (confidence={confidence:.3f})\n\n")
        else:
            min_support = self.min_support_entry.get()
            if not min_support:
                messagebox.showwarning("Missing Parameter", "Please enter the minimum support value.")
                return     
            data=Load_data(self.dataset_path)
            rules=CloseAlgorithm(data, float(min_support))      
            # Display the association rules in a new window
            rule_window = tk.Toplevel(self.master)
            rule_window.title("Association Rules")
            rule_text = tk.Text(rule_window, wrap=tk.WORD)
            rule_text.pack()
            # Print the rules    
            for key, value in rules.items():
                rule_text.insert(tk.END, f"{key} --> {value}\n\n")
root = tk.Tk()
gui = AssociationRulesGUI(root)
root.mainloop()

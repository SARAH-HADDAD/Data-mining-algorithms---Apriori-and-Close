import tkinter as tk
from tkinter import filedialog
import apriori

class App:
    def __init__(self, master):
        self.master = master
        master.title("Association Rule Mining")

        # Create a menu bar
        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        master.config(menu=menu_bar)

        # Create a frame to hold the widgets
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Create a label and a scale for minimum support
        self.support_label = tk.Label(self.frame, text="Minimum Support:")
        self.support_label.grid(row=0, column=0)
        self.support_scale = tk.Scale(self.frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.support_scale.set(0.1)
        self.support_scale.grid(row=0, column=1)

        # Create a label and a scale for minimum confidence
        self.confidence_label = tk.Label(self.frame, text="Minimum Confidence:")
        self.confidence_label.grid(row=1, column=0)
        self.confidence_scale = tk.Scale(self.frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.confidence_scale.set(0.5)
        self.confidence_scale.grid(row=1, column=1)

        # Create a button to run the algorithm
        self.run_button = tk.Button(self.frame, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=2, column=0, columnspan=2)

    def open_file(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
        
    def run_algorithm(self):
        # Get the minimum support and confidence from the scales
        min_support = self.support_scale.get()
        min_confidence = self.confidence_scale.get()

        # Load the data from the selected file
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        data = apriori.load_data(self.file_path)

        # Get the frequent itemsets and association rules
        frequent_itemsets = apriori.get_frequent_itemsets(data, min_support)
        association_rules = apriori.get_association_rules(frequent_itemsets, min_confidence, data)

        # Display the association rules in a new window
        rule_window = tk.Toplevel(self.master)
        rule_window.title("Association Rules")
        rule_text = tk.Text(rule_window, wrap=tk.WORD)
        rule_text.pack()
        for antecedent, consequent, confidence in association_rules:
            rule_text.insert(tk.END, f"{set(antecedent)} => {set(consequent)} (support={min_support:.3f}, confidence={confidence:.3f})\n\n")

# Create the main window
root = tk.Tk()
app = App(root)
root.mainloop()

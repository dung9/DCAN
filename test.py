import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Treeview Example")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Name", "Age"), show='headings')
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")

# Insert some data
tree.insert("", "end", iid="1", values=("Alice", 30))
tree.insert("", "end", iid="2", values=("Bob", 25))

# Function to update the item by iid
def update_item(iid, new_values):
    tree.item(iid, values=new_values)

# Update the item with iid "1"
update_item("1", ("Alice", 31))

# Pack the Treeview widget
tree.pack()

# Run the application
root.mainloop()
import pandas as pd
import tkinter as tk
import PickAProject as pp
import numpy as np
from tkinter import ttk

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize app
        self.title("PickAProject")
        self.project_picker = pp.PickAProject()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ProjectsDisplay(self, self.project_picker)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")


class ProjectsDisplay(ttk.Frame):
    def __init__(self, parent, pp: pp.PickAProject):
        super().__init__()
        self.pp = pp
        self.df: pd.DataFrame = self.pp.get_df()
        self.project_names = self.get_project_names()   # dict {index, name}
        self.columns = self.df.columns.tolist()
        self.entries: list[ttk.Entry] = []
        self.listboxes: list[tk.Listbox] = []
        self.num_columns: int = len(self.df.columns)

        for i in range(self.num_columns):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(2, weight=1)

            # Above Entries: labels
            label = ttk.Label(self, text=self.df.columns[i])
            label.grid(row=1, column=i, sticky="ew")
            label.bind("<Button-1>", lambda event, col = i: self.sort_df(col))

            # Top of Frame: Entry field for projects
            entry = ttk.Entry(self)
            entry.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.entries.append(entry)  # Creates list of entries that we can access later

            
            # Under Entries: ListBoxes
            listbox = tk.Listbox(self)
            listbox.grid(row=2, column=i, padx=5, pady=5, sticky="nsew")
            self.listboxes.append(listbox)  # Creates list of listboxes that we can access later

        self.fill_lists()

        # Button to add new projects
        add_button = ttk.Button(self, text="Add Project", command=self.add_project)
        add_button.grid(row=0, column=self.num_columns + 1, padx=2, pady=2)

        # Button to remove projects
        remove_button = ttk.Button(self, text="Remove Project", command=self.remove_project)
        remove_button.grid(row=1, column=self.num_columns + 1, padx=2, pady=2)

        # Button to edit value
        self.edit_frame = ttk.Frame(self)
        self.edit_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.edit_frame.columnconfigure(0, weight=1)
        self.edit_frame.rowconfigure(0, weight=1)

        self.edit_entry = ttk.Entry(self.edit_frame)
        self.edit_entry.grid(row=0, column=0, padx=2, pady=5, sticky="e")
        self.edit_entry.bind("<Return>", self.edit_selection)

        edit_button = ttk.Button(self.edit_frame, text="Edit Value", command=self.edit_selection)
        edit_button.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        # Filter frame
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.grid(row=2, column=self.num_columns+1, padx=2, pady=2, sticky="nsew")
        # self.filter_frame.columnconfigure(0, weight=1)
        # self.filter_frame.columnconfigure(1, weight=1)
        # self.filter_frame.rowconfigure(0, weight=1)
        # self.filter_frame.rowconfigure(1, weight=1)
        # self.filter_frame.rowconfigure(2, weight=1)

        filter_label = ttk.Label(self.filter_frame, text="Filter by:")
        filter_label.grid(row=0, column=0, padx=2, pady=2, sticky="nw", rowspan=2)

        self.column_filter_frame = ttk.Frame(self.filter_frame)
        self.column_filter_frame.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

        column_filter_label = ttk.Label(self.column_filter_frame, text="Column")
        column_filter_label.grid(row=0, column=0, sticky="n")
        self.filter_cols = ttk.Combobox(self.column_filter_frame, values=self.columns, state="readonly")
        self.filter_cols.grid(row=1, column=0, padx=5, pady=2, sticky="new")
        self.filter_cols.bind("<<ComboboxSelected>>", self.select_column_filter)

        self.value_filter_frame = ttk.Frame(self.filter_frame)
        self.value_filter_frame.grid(row=1, column=1, sticky="nsew")
        value_filter_label = ttk.Label(self.value_filter_frame, text="Value")
        value_filter_label.grid(row=0, column=0, sticky="n")
        self.filter_vals = ttk.Combobox(self.value_filter_frame, state="readonly")
        self.filter_vals.grid(row=1, column=0, padx=5, pady=2, sticky="new")
        self.filter_vals.bind("<<ComboboxSelected>>", self.select_value_filter)

        self.column_filter = None
        self.value_filter = None

        self.filter_button_frame = ttk.Frame(self.filter_frame)
        self.filter_button_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.filter_button = ttk.Button(self.filter_button_frame, text="Apply Filter", command=lambda: self.update_filter(self.column_filter, self.value_filter))
        self.filter_button.grid(row=0, column=0)

        self.clear_filter_button = ttk.Button(self.filter_button_frame, text="Clear Filter", command=self.reset_filter)
        self.clear_filter_button.grid(row=1, column=0)

        self.project_picker = ttk.Frame(self)
        self.project_picker.grid(row=3, column=self.num_columns+1)

        self.pick_project_button = ttk.Button(self.project_picker, text="Choose Project", command=self.pick_project)
        self.pick_project_button.grid(row=0, column=0)
        self.chosen_project = ttk.Label(self.project_picker, text="No Project Chosen")
        self.chosen_project.grid(row=1, column=0)

    def pick_project(self):
        project = self.pp.pick_project()
        self.chosen_project.config(text=project)

    def select_column_filter(self, event: tk.Event):
        self.column_filter = self.filter_cols.get()
        self.value_filter = None

        self.filter_vals.set("")
        self.filter_vals["values"] = self.get_values(self.column_filter)

    def select_value_filter(self, event: tk.Event):
        self.value_filter = self.filter_vals.get()

    def update_filter(self, col, val):
        self.pp.gui_filter_search(col, val)
        self.update()

    def reset_filter(self):
        self.column_filter = None
        self.value_filter = None
        self.filter_cols.set("")
        self.filter_vals.set("")
        self.filter_vals["values"] = []
        self.pp.reset_filter()
        self.update()

    def get_values(self, col):
        df = self.pp.get_df(filtered=False)
        return sorted(i for i in list(set(df[col].tolist())))

    def edit_selection(self, event: tk.Event):
        row, col = self.get_selection()
        # print(self.project_names[row])
        self.pp.edit_project(project_name=self.project_names[row], column=self.columns[col], new_value=self.edit_entry.get())
        self.edit_entry.delete(0, tk.END)
        self.update()
        
    def get_selection(self):    # returns tuple: (row,col)
        for i in range(len(self.listboxes)):
            if self.listboxes[i].curselection():  # if something in this listbox is selected, go to next
                selection = (self.listboxes[i].curselection()[0], i)

        return selection

    def sort_df(self, col:int):
        self.pp.sort_projects(self.columns[col])
        self.update()

    def update(self):
        self.df = self.pp.get_df(filtered=True)
        self.project_names = self.get_project_names()   # dict {index, name}
        self.columns = self.df.columns.tolist()
        self.fill_lists()

    def add_project(self):
        self.pp.add_project(self.entries[0].get(), self.entries[1].get(), self.entries[2].get(), self.entries[3].get())
        self.update()

        # Clear entries
        for i in self.entries:
            i.delete(0, tk.END)

    def remove_project(self):
        selections = np.array([])

        # Get index for all selected options
        for i in self.listboxes:
            selections = np.append(selections, i.curselection())
        selections = np.unique(selections)

        if not selections:  # return empty if nothing is selected
            return

        names = self.get_project_names()
        for i in selections:
            self.pp.complete_project(names[i])

        self.update()

    def get_project_names(self):
        return dict(enumerate(self.df["project_name"]))

    def fill_lists(self):
        for i in range(self.num_columns):
            # clear list
            self.listboxes[i].delete(0, tk.END)

            # Refill lists
            items: list[str] = self.df.iloc[:,i].fillna("").tolist()
            self.listboxes[i].insert(tk.END, *items)

main()

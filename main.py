import pandas as pd
import numpy as np
import random 
# r"C:\Users\Tyler\Desktop\Tyler\Coding Projects\PickAProject\projects_list.csv" Lab Desktop
# r"C:\Users\Tyler\Documents\Tyler\Coding Projects\PickAProject\projects_list.csv" Laptop
class PickAProject:
    type str_list = list[str]
    def __init__(self, project_type:str = "", difficulty:str = "", projects_path = r"C:\Users\Tyler\Desktop\Tyler\Coding Projects\PickAProject\projects_list.csv"):
        self.projects_path = projects_path
        self.project_type = project_type.lower()
        self.difficulty = difficulty.lower()
        self.projects_df: pd.DataFrame = pd.read_csv(projects_path)
        self.columns = {c.lower(): c for c in self.projects_df.columns} # {lower: Original}

        self.filter_projects()

    def filter_projects(self):
        # This method updates the filtered df
        self.projects_filtered = self.projects_df
        if self.project_type != "":
            self.projects_filtered = self.projects_filtered[self.projects_filtered["type"].str.lower() == self.project_type]
        
        if self.difficulty != "":
            self.projects_filtered = self.projects_filtered[self.projects_filtered["difficulty"].str.lower() == self.difficulty]
        

    def add_projects(self, project_name: str_list, difficulty: str_list, language: str_list, type: str_list):
        # Adds multiple projects with inputs in the form of list[str]
        if len(project_name) != len(difficulty) != len(language) != len(type):
            print("Length of lists need to be same, currently: \n project_name: " + len(project_name) + "\n difficulty: " + len(difficulty) + "\n language: " + len(language) + "\n type: " + len(type))
            return

        lst = []
        for i in range(len(project_name)):
            # Check if project with name already exists in database
            if self.project_exists(project_name[i]):
                print("project with name " + project_name[i] + " already exists, skipping.")

            # Only add new row to list if project name does not exist
            else:
                new_row = [project_name[i], difficulty[i], language[i], type[i]]
                lst.append(new_row)

        # If all added projects already exist, then nothing happens
        if len(lst) == 0:
            print("No projects were added")
            return

        # Construct dataframe and concatinate with full df
        df_add = pd.DataFrame(lst, columns=self.projects_df.columns)
        self.projects_df = pd.concat([self.projects_df, df_add], ignore_index=True)

        # Update csv and filtered search
        self.print_csv()
        self.filter_projects()
        print(self.projects_df)

    def print_csv(self):
        self.projects_df.to_csv(self.projects_path, index=False)

    def find_column(self, column:str):
        # Checks columns dictionary for matches, returns the correct name for column
        lw = column.strip().lower()
        if lw not in self.columns:
            print("Column titled '" + column + "' does not exist.")
            return
        return self.columns[lw]

    def add_project(self, project_name: str, difficulty: str, language: str, type: str):
        # Adds only 1 project to the database

        # Check if project name already exists in database, return if true
        if self.project_exists(project_name):
            print("Project with that name already exists.")
            return
        
        new_row = [[project_name, difficulty, language, type]]
        # Construct dataframe and concatinate
        df_add = pd.DataFrame(new_row, columns=self.projects_df.columns)
        self.projects_df = pd.concat([self.projects_df, df_add], ignore_index=True)

        # Update csv and filter
        self.print_csv()
        self.filter_projects()
        print(self.projects_df)

    def project_exists(self, project_name: str):
        # Checks database for matching project names, returns true if it already exists
        names_lst = [i.lower() for i in self.projects_df["project_name"] if i.strip().lower() == project_name.strip().lower()]
        return len(names_lst) != 0


    def view_projects(self, all:bool = True):
        if all:
            print(self.projects_df)
        else:
            if len(self.projects_filtered) == 0:
                print("There were no projects with your filters. ")
                return
            print(self.projects_filtered)

    def search_projects(self, project_type:str = "", difficulty:str = "", language:str = ""):
        # Updates filters for projects
        if project_type.lower() != self.project_type.lower():
            self.project_type = project_type.lower()
        if difficulty.lower() != self.difficulty.lower():
            self.difficulty = difficulty.lower()
        self.filter_projects()
        self.view_projects(all = False)

    def sort_projects(self, column:str):
        col = self.find_column(column)
        if col == None: return
        
        self.projects_df = self.projects_df.sort_values(col).reset_index(drop=True)
        self.filter_projects()
        self.view_projects()

    def edit_project(self, project_name:str, column:str, new_value:str):
        # Make changes to a project in the database, change language, difficulty, type

        
        # Check that project name exists
        if not self.project_exists(project_name):
            print("Project with name '" + project_name + "' does not exist in database.")
            return

        # Check that requested column exists
        col = self.find_column(column)
        if col == None: return

        mask = self.projects_df["project_name"].str.lower() == project_name.lower()
        
        self.projects_df.loc[mask, col] = new_value
        self.print_csv()
        self.filter_projects()
        print(self.projects_df.loc[mask])

    def pick_project(self, filtered:bool = True):
        if filtered:
            num_projects = len(self.projects_filtered)
            rand_idx = random.randint(0, num_projects-1)
            chosen_project = self.projects_filtered.iloc[rand_idx]

        else:
            num_projects = len(self.projects_df)
            rand_idx = random.randint(0, num_projects-1)
            chosen_project = self.projects_df.iloc[rand_idx]

        print("Your chosen project is '" + chosen_project['project_name'] + "'! \n Good Luck!")

    def complete_project(self, project_name:str):
        # This is the method to remove a project from the database
        if not self.project_exists(project_name):
            print("Project with name '" + project_name + "' does not exist.")
            return

        self.projects_df = self.projects_df.drop(self.projects_df[self.projects_df["project_name"].str.lower() == project_name.lower()].index)
        self.print_csv()
        self.filter_projects()
        print("Congratulations for finishing the '" + project_name + "' project! \n You deserve a beer!")
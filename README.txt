This project picker is just a way for my indecisive brain to get a project to work on.
It has a database: projects_list.csv, which keeps all the projects in one place.
Data structure:
    columns: ["project_name", "difficulty", "language", "type"]
    each row is a new project, with the other columns being features I can search for.

Syntax:
    PickAProject(project_type:str (optional), difficulty:str (optional),
                projects_path:str (optional))
        ## initializes project picker class, the properties are by default = "" and they only change the filtered list of projects
    
    project.add_projects(project_name: List[str], 
                                difficulty: List[str],
                                language: List[str],
                                type: List[str])
        ## This is how you add a multiple new projects to the database
        ## the properties are in lists so that it is possible to add multiple projects at once
        ## Every property must be a list of the same size

    project.add_project(project_name: str, 
                                difficulty: str,
                                language: str,
                                type: str)
        ## This is how you add one new project to the database
        ## Every property must be a entered

    project.search_projects(project_type:str (optional),
                            difficulty:str (optional),
                            language:str (optional))
        ## This method updates the search filters to find specific projects.
        ## Search is not case sensitive
        ## By default all properties are = "", so calling this method with no properties shows ALL projects
    
    project.view_projects(all:bool (optional))
        ## This method spits out a view of the projects database.
        ## by default all = True, showing all projects in the database. Set this to False to only show filtered projects

    
import config
import tableauserverclient as TSC 

server = config.conf["server"]
site = config.conf["site"]
username = config.conf["username"]
password = config.conf["password"]
new_project = config.conf["new_project"]
project_list = config.conf["project_list"]

def create_and_populate_new_project(server, site, username, password, project_list, new_project):
    '''
    Amalgamates projects into a new, empty project.

            Parameters:
                    server (str): Specified server address.
                    site (str):  The name of the site that the user is signed into.
                    username (str): the user with appropriate access' username.
                    password (str): the same user's password.
                    project_list (list(str)): List of projects to be amalgamated.
                    archive_project (str): The new project, made of an amalgamation of   
                                           the workbooks in projects in the project_list.

            Returns:
                    None
    '''

    tableau_auth = TSC.PersonalAccessTokenAuth(username, password, site_id=site)
    server = TSC.Server(server, use_server_version=True)
    with server.auth.sign_in(tableau_auth):
        
        # Chech a project with name X doesn't already exist. 

        all_project_items = server.projects.get()
        project_list = []

        for project in all_project_items: 
            project_list.append(project.name)

        if new_project in project_list: 
            return print("New project name, {new_project}, already exists. Try another name".format())


        else: 
            # Create a new project. 
            new_project = TSC.ProjectItem(name=new_project, content_permissions='LockedToProject', description='Amalgamation of projects: {}'.format(*project_list))
            server.projects.create(new_project)

            # Check the project now exits.
            all_project_items = server.projects.get()
            project_list = []

            for project in all_project_items: 
                project_list.append(project.name)

            if new_project not in project_list: 
                return print("New project, {}, not created.".format(new_project))


            else: 
                # Get all workbooks
                all_workbooks = server.workbooks.get()
                
                for workbook in all_workbooks: 

                    # Check the new project is empty 
                    if workbook.project_name == new_project: 
                        return print("Project not empty. Check the project, {}, to find out he issue.".format(new_project)) 


                # For the workbook that are in one of the projects to be amalgamated, 
                # move to the new, empty project called X.
                for workbook in all_workbooks: 

                    if workbook.project_name in project_list: 

                        workbook.project_name = new_project
                        server.workbooks.update(workbook)

def check_workbook_migration_and_delete(server, site, username, password, project_list):
    '''
    Checks projects are empty and if so, deletes them.

            Parameters:
                    server (str): Specified server address.
                    site (str):  The name of the site that the user is signed into.
                    username (str): the user with appropriate access' username.
                    password (str): the same user's password.
                    project_list (list(str)): List of projects to be amalgamated.
                    archive_project (str): The new project, made of an amalgamation of   
                                           the workbooks in projects in the project_list.

            Returns:
                    None
    '''

    tableau_auth = TSC.PersonalAccessTokenAuth(username, password, site_id=site)
    server = TSC.Server(server, use_server_version=True)
    with server.auth.sign_in(tableau_auth):
        
        # Get all workbooks and make sure none exist in the list of projects to delete.
        all_workbooks = server.workbooks.get()
        
        for workbook in all_workbooks: 

            if workbook.project_name in project_list: 
                return print("Project {} not empty. Make sure to empty it before deleting".format(workbook.project_name))

        # Check for projects with duplicated names
        all_projects = server.projects.get()
        all_projects_names = []
        for project in all_projects: 
            all_projects_names.append(project.name)

        project_IDs = []
        for project_name in project_list:

            # Check for projects with duplicated names
            if all_projects_names.count(project_name) > 1: 
                return print("There is more than one project with the name {}, therefore it cannot be deleted.".format(project_name))
            
            # Use project names to find project IDs, and append those to an IDs list
            project = [proj for proj in TSC.Pager(server.projects) if proj.name == project_name]
            project_IDs.append(project[0].id)

        # Delete each project, using it's ID
        for project_ID in project_IDs:
        
            server.projects.delete(str(project_ID))

if __name__ == "__main__":
    create_and_populate_new_project(server, site, username, password, project_list, new_project)
    check_workbook_migration_and_delete(server, site, username, password, project_list)

import tableauserverclient as TSC
import config

server = config.conf["server"]
site = config.conf["site"]
username = config.conf["username"]
password = config.conf["password"]
workbook_to_move = config.conf["workbooks"]
archive_project = config.conf["archive_project"]



def main(server, site, username, password, workbook_to_move, archive_project):
    '''
    Moves workbooks inside a tableau server to an assigned "Archive" folder.

            Parameters:
                    server (str): Specified server address
                    site (str):  The name of the site that the user is signed into.
                    "password" (str): "password",
                    "workbooks" (list(str)): List of workbooks names to be moved
                    "archive_project" (str): Destination project.

            Returns:
                    None
    '''

    # Step 1: Sign in to server
    tableau_auth = TSC.PersonalAccessTokenAuth(username, password, site_id=site)
    server = TSC.Server(server, use_server_version=True)
    with server.auth.sign_in(tableau_auth):

        # Step 2: Ensure the workbook exits on the server.
        all_workbooks = server.workbooks.get()
        all_workbooks_list = []

        for i in len(all_workbooks): 
            all_workbooks_list.append(all_workbooks[i].name)

        all_workbooks_set = set(all_workbooks_list)
        intersection = all_workbooks_set.intersection(workbook_to_move)
        workbook_list = list(intersection)

        # Step 3: Find destination project
        for workbook_name in workbook_list:
            try:
                dest_project = server.projects.filter(name=archive_project)[0]
            except IndexError:
                raise LookupError(f"No project named {archive_project} found.")

            # Step 4: Query workbook/workbooks to move
            try:
                workbooks = server.workbooks.filter(name=workbook_name)
            except IndexError:
                raise LookupError(f"No workbook named {workbook_name} found")

            for i in len(workbooks): 
                workbook = workbooks[i]
                # Step 5: Update workbook with new project id
                workbook.project_id = dest_project.id
                server.workbooks.update(workbook)

        server.auth.sign_out()

if __name__ == "__main__":
    main(server, site, username, password, workbook_to_move, archive_project)
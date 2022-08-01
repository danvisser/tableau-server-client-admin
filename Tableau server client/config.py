import pandas as pd

conf = { 
    "server": "server",
    "site": "site",
    "username": "username",
    "password": "password",
    "workbooks": pd.read_csv("list_of_workbooks.csv")["workbook_names"].to_csv(),
    "archive_project": "archive_project"
}
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conditions
import database


def add_folder_clicked():
    folder_path = QFileDialog.getExistingDirectory()
    # folder_path will be a empty string if no directory is choosen,
    # and an empty string evaluates to false in python
    if folder_path:
        folder = QDir(folder_path)
        selected_folder = folder.dirName()
        conn = database.sql_connection()
        database.folder_table(conn)
        values = (selected_folder, str(folder_path))
        if database.sql_insert(conn, values):
            # After insertion of a folder, no folder will be selected
            return True
            print("F Records Inserted")
        else:
            return False
            print("F Records not Inserted")


def resume_pause_clicked(dry_run, path, rule):
    rule_conditions = database.retrieve_values(path, rule)
    todo, file_paths = conditions.get_files(rule_conditions)
    if not dry_run:
        for file, values in todo.items():
            action = values[0]
            category = values[1]
            print(file)
            print(action)
            conditions.run_task(rule_conditions, action, file)
        return list()
    else:
        return file_paths


def remove_folder_button_clicked():
    return database.remove_folder()
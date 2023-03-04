import sqlite3
from sqlite3 import Error
import conditions
from PyQt5.QtSql import QSqlDatabase
from rule_conditions import RuleConditions


retrieved_list = []

def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error as er:
        print(er)



def folder_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists FOLDER(
ID      integer        PRIMARY KEY      AUTOINCREMENT,
Folder_Name   TEXT             NOT NULL,
Folder_Path   TEXT             NOT NULL,
unique (Folder_Path))""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def rule_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE if not exists RULE(
F_ID      integer            NOT NULL,
Rule_Name   TEXT             NOT NULL PRIMARY KEY,
State       integer,
FOREIGN KEY(F_ID) REFERENCES FOLDER(ID))""")
    except Error as er:
        print(er)
    finally:
        con.commit()


def sql_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO FOLDER(Folder_Name, Folder_Path) VALUES(?, ?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def get_folder_id(folder_path=None):
    conn = sql_connection()
    c = conn.cursor()
    c.execute('select ID from FOLDER where Folder_Path = ?', [folder_path])
    folder_id = c.fetchone()
    folder_id = str(folder_id)[1:-2]
    return folder_id


def condition_table(con):
    try:
        cursor = con.cursor()
        cursor.execute("""
        CREATE TABLE if not exists CONDITIONS(
        Rule         Text,
        Condition    Text,
        Operator     Text,
        Size         double,
        Extension    Text,
        Date         Text,
        Unit         Text,
        Actions      Text,
        Target_Path  Text,
        Rename       Text,
        unique (Rule),
        FOREIGN KEY(Rule) REFERENCES RULE(Rule_Name))
        """)
    except Error as er:
        print(er)
    finally:
        con.commit()


def insertCondition(value):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO CONDITIONS(Rule) VALUES(?)', [value])
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def retrieve_values(path, rule):
    con = sql_connection()
    retrieved_list = []
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM CONDITIONS WHERE Rule = ?', [rule])
        for row in cursor.fetchall():
            row = str(row)[1:-1]
            retrieved_list.append(row)
        retrieved_list = retrieved_list[0].split(",")
        rule_name = retrieved_list[0][1:-1]
        condition_value = retrieved_list[1][2:-1]
        operator_value = retrieved_list[2][2:-1]
        size_value = retrieved_list[3][1:]
        ext_value = retrieved_list[4][2:-1]
        date_edit_value = retrieved_list[5][2:-1]
        unit_value = retrieved_list[6][2:-1]
        actions_value = retrieved_list[7][2:-1]
        target_path = retrieved_list[8][2:-1]
        rename_value = retrieved_list[9][2:-1]
        rule_conditions = RuleConditions(rule_name, condition_value, operator_value, size_value,
            ext_value, date_edit_value, unit_value, actions_value, path, target_path, rename_value)
        con.commit()
        return rule_conditions
    except Error as er:
        print(er)
    finally:
        con.close()



def remove_folder(selected_folder):
    con = sql_connection()
    try:
        if selected_folder:
            cursor = con.cursor()
            cursor.execute('DELETE FROM CONDITIONS WHERE Rule IN (SELECT Rule_Name FROM RULE WHERE F_ID IN (SELECT ID '
                           'FROM FOLDER WHERE Folder_Path = ?))', [selected_folder])
            cursor.execute('DELETE FROM RULE WHERE F_ID IN (SELECT ID FROM FOLDER WHERE Folder_Path = ?)',
                           [selected_folder])
            cursor.execute('DELETE FROM FOLDER WHERE Folder_Path = ?', [selected_folder])
            return True
        else:
            return False
    except Error as er:
        print(er)
    finally:
        con.commit()


def remove_rule(selected_rule):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('DELETE FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        cursor.execute('DELETE FROM RULE WHERE Rule_Name = ?', [selected_rule])
    except Error as er:
        print(er)
    finally:
        con.commit()


def update_condition_rule(selected_rule, name):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('UPDATE CONDITIONS SET Rule = ? WHERE Rule = ?', (name, selected_rule))
        return True
    except Error as er:
        print(er)
        return False
    finally:
        con.commit()


def init_database():
    con = sql_connection()
    folder_table(con)
    rule_table(con)
    condition_table(con)


def setup_database(self):
        init_database()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database.db")
        db.open()

# For background helper
def get_folders_list():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('SELECT Folder_Path FROM FOLDER')
        list_without_tuples = []
        for path in cursor.fetchall():
            list_without_tuples.append(str(path)[2:-3])
        return list_without_tuples
    except Error as er:
        print(er)

def get_rules_list(f_path):
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('SELECT Rule_Name FROM Rule WHERE F_ID = (SELECT ID FROM FOLDER WHERE Folder_Path = ?) AND State = (2)', [f_path])
        list_without_tuples = []
        for path in cursor.fetchall():
            list_without_tuples.append(str(path)[2:-3])
        return list_without_tuples
    except Error as er:
        print(er)
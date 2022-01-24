import sqlite3
from sqlite3 import Error
import conditions

selected_rule = ''
selected_folder = ''
retrieved_list = []


def getSelectedRule(rule):
    global selected_rule
    selected_rule = rule.data()


def getSelectedFolder(folder):
    global selected_folder
    selected_folder = folder.data()


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


def rule_insert(con, values):
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO RULE(F_ID, Rule_Name) VALUES(?, ?)', values)
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def get_folder_id():
    conn = sql_connection()
    folder_name = selected_folder
    c = conn.cursor()
    c.execute('select ID from FOLDER where Folder_Name = ?', [folder_name])
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
        unique (Rule))
        """)
    except Error as er:
        print(er)
    finally:
        con.commit()


def insertCondition(value):
    value = value.data()
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('INSERT INTO CONDITIONS(Rule) VALUES(?)', [value])
        con.commit()
        return True
    except Error as er:
        print(er.args)
        return False


def retrieve_folder_path():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('SELECT Folder_Path FROM FOLDER WHERE Folder_Name = ?', [selected_folder])
        conditions.original_path = str(cursor.fetchone())[3:-4]
    except Error as er:
        print(er)
    finally:
        con.commit()


def retrieve_values():
    con = sql_connection()
    global retrieved_list
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        for row in cursor.fetchall():
            row = str(row)[1:-1]
            retrieved_list.clear()
            retrieved_list.append(row)
        retrieved_list = retrieved_list[0].split(",")
        conditions.rule_name = retrieved_list[0][1:-1]
        conditions.condition_value = retrieved_list[1][2:-1]
        conditions.operator_value = retrieved_list[2][2:-1]
        conditions.size_value = retrieved_list[3][1:]
        conditions.ext_value = retrieved_list[4][2:-1]
        conditions.date_edit_value = retrieved_list[5][2:-1]
        conditions.unit_value = retrieved_list[6][2:-1]
        conditions.actions_value = retrieved_list[7][2:-1]
        conditions.target_path = retrieved_list[8][2:-1]
        conditions.rename_value = retrieved_list[9][2:-1]
        # print(conditions.rule_name, conditions.condition_value, conditions.operator_value, conditions.size_value,
        #       conditions.ext_value, conditions.date_edit_value, conditions.unit_value, conditions.actions_value,
        #       conditions.target_path, conditions.rename_value)
    except Error as er:
        print(er)
    finally:
        con.commit()


def remove_folder():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('DELETE FROM CONDITIONS WHERE Rule IN (SELECT Rule_Name FROM RULE WHERE F_ID IN (SELECT ID '
                       'FROM FOLDER WHERE Folder_Name = ?))', [selected_folder])
        cursor.execute('DELETE FROM RULE WHERE F_ID IN (SELECT ID FROM FOLDER WHERE Folder_Name = ?)',
                       [selected_folder])
        cursor.execute('DELETE FROM FOLDER WHERE Folder_Name = ?', [selected_folder])
    except Error as er:
        print(er)
    finally:
        con.commit()


def remove_rule():
    con = sql_connection()
    try:
        cursor = con.cursor()
        cursor.execute('DELETE FROM CONDITIONS WHERE Rule = ?', [selected_rule])
        cursor.execute('DELETE FROM RULE WHERE Rule_Name = ?', [selected_rule])
    except Error as er:
        print(er)
    finally:
        con.commit()


def init_database():
    con = sql_connection()
    folder_table(con)
    rule_table(con)
    condition_table(con)

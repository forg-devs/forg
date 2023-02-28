import os
import actions
import datetime
import sys
import decimal

rule_name = ''
condition_value = ''  # combobox_value
operator_value = ''   # combobox1_value
size_value = ''
ext_value = ''
date_edit_value = ''
unit_value = ''
actions_value = ''
original_path = r''
target_path = r''
rename_value = ''
filtered_files = []

# https://stackoverflow.com/a/14996816
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

size_base = 1000
# Windows file explorer shows values in KiB, MiB..., but labels it KB, MB...
# https://imgs.xkcd.com/comics/kilobyte.png
# We shouldn't be doing this, but most of the windows user will use file explorer
# to check sizes and they'd think it's our application that's wrong
if sys.platform == 'win32':
    size_base = 1024


def human_size(n_bytes):
    # TODO: Due to our database value being float,
    # it will always have 1 decimal number, i.e '0'
    # even if user entered an integer
    # https://stackoverflow.com/a/6190291
    no_of_decimals = abs(decimal.Decimal(str(size_value)).as_tuple().exponent)
    print("No of decimals: {}".format(no_of_decimals))
    unit = unit_value
    i = 0
    while unit != suffixes[i]:
        n_bytes /= size_base
        i += 1
    result = '{:.{}f}'.format(n_bytes, no_of_decimals)
    # Windows file explorer doesn't show decimal value
    # for items above 100 non-decimal value.
    # We shouldn't be handling this, but Harshit282 wants it,
    # so add it.
    if sys.platform == 'win32':
        value = float(result)
        if int(value) >= 100:
            return int(value)

    return float(result)


def get_files():
    todo = {}
    filtered_files.clear()
    for subdir, dirs, files in os.walk(original_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if condition_value == 'Extension':
                if operator_value == 'is':
                    if file_path.endswith(ext_value):
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                elif operator_value == 'is not':
                    if file_path.endswith(ext_value):
                        pass
                    else:
                        filtered_files.append(file)
                        todo[file_path] = actions_value

            elif condition_value == 'Date Added':
                dt = datetime.datetime.strptime(date_edit_value, '%Y-%m-%d')
                new_dt = int(dt.strftime('%Y%m%d'))
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y%m%d'))
                if operator_value == 'is':
                    if new_dt == file_date:
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                if operator_value == 'is before':
                    if new_dt > file_date:
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                if operator_value == 'is after':
                    if new_dt < file_date:
                        filtered_files.append(file)
                        todo[file_path] = actions_value

            elif condition_value == 'Size':
                global size_value
                size_value = float(size_value)
                if operator_value == 'is':
                    size_of_file = human_size(os.path.getsize(file_path))
                    print("Calculated size of file: {}".format(size_of_file))
                    print("Size given in condition: {}".format(size_value))
                    if size_of_file == size_value == 0:
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                    elif size_of_file == size_value:
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                elif operator_value == 'greater than':
                    size_of_file = human_size(os.path.getsize(file_path))
                    if size_of_file > size_value:
                        filtered_files.append(file)
                        todo[file_path] = actions_value
                elif operator_value == 'less than':
                    size_of_file = human_size(os.path.getsize(file_path))
                    if size_of_file < size_value:
                        filtered_files.append(file)
                        todo[file_path] = actions_value

    return todo


def run_task(action_performed, file_to_process):  # file_to process == a
    global target_path
    if action_performed == 'Copy':
        actions.copy(file_to_process, target_path)
    elif action_performed == 'Move':
        actions.move(file_to_process, target_path)
    elif action_performed == 'Delete':
        actions.delete(file_to_process)
    elif action_performed == 'Trash Bin':
        actions.trash_bin(file_to_process)
    elif action_performed == 'Rename':
        actions.rename(file_to_process, rename_value)

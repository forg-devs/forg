import os
import Rules
import datetime
import sys
import decimal

rule_name = ''
condition_value = ''  # combobox_value
operator_value = ''   # combobox1_value
size_value = 0.0
ext_value = ''
date_edit_value = ''
unit_value = ''
actions_value = ''
original_path = r''
target_path = r''
rename_value = ''


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
    # https://stackoverflow.com/a/6190291
    # TODO: Due to our database value being float,
    # it will always have 1 decimal number, i.e '0'
    # even if user entered an integer
    no_of_decimals = abs(decimal.Decimal(str(size_value)).as_tuple().exponent)
    print("no_of_decimals")
    print(no_of_decimals)
    unit = unit_value
    i = 0
    while n_bytes >= size_base and unit != suffixes[i]:
        n_bytes /= size_base
        i += 1
    result = '{:.{}f}'.format(n_bytes, no_of_decimals)
    return float(result)


def conditions_applied():
    if condition_value == 'Extension':
        if operator_value == 'is':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    if a.endswith(ext_value):
                        run_task(actions_value, a)
        elif operator_value == 'is not':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    if a.endswith(ext_value):
                        pass
                    else:
                        run_task(actions_value, a)

    if condition_value == 'Date Added':
        dt = datetime.datetime.strptime(date_edit_value, '%Y-%m-%d')
        new_dt = int(dt.strftime('%Y%m%d'))
        for subdir, dirs, files in os.walk(original_path):
            for file in files:
                a = os.path.join(subdir, file)
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(a)).strftime('%Y%m%d'))
                if operator_value == 'is':
                    if new_dt == file_date:
                        run_task(actions_value, a)
                if operator_value == 'is before':
                    if new_dt > file_date:
                        run_task(actions_value, a)
                if operator_value == 'is after':
                    if new_dt < file_date:
                        run_task(actions_value, a)

    if condition_value == 'Size':
        if operator_value == 'is':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    print("size of file")
                    print(size_of_file)
                    print("condition_value")
                    print(size_value)
                    if size_of_file == size_value == 0:
                        run_task(actions_value, a)
                    elif size_of_file == size_value:
                        run_task(actions_value, a)
        elif operator_value == 'greater than':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file > size_value:
                        run_task(actions_value, a)
        elif operator_value == 'less than':
            for subdir, dirs, files in os.walk(original_path):
                for file in files:
                    a = os.path.join(subdir, file)
                    size_of_file = human_size(os.path.getsize(a))
                    if size_of_file < size_value:
                        run_task(actions_value, a)


def run_task(action_performed, file_to_process):  # file_to process == a
    global target_path
    if action_performed == 'Copy':
        Rules.copy(file_to_process, target_path)
    elif action_performed == 'Move':
        Rules.move(file_to_process, target_path)
    elif action_performed == 'Delete':
        Rules.delete(file_to_process)
    elif action_performed == 'Trash Bin':
        Rules.trash_bin(file_to_process)
    elif action_performed == 'Rename':
        Rules.rename(file_to_process, rename_value)

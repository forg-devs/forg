import os
import actions
import datetime
import sys
import decimal


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

def get_file_category(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext in ['.jpg', '.png', '.gif', '.bmp']:
        return 'Images'
    elif ext in ['.pdf', '.doc', '.txt', '.xlsx']:
        return 'Documents'
    elif ext in ['.mp4', '.avi', '.wmv', '.mov']:
        return 'Videos'
    elif ext in ['.mp3', '.flac', '.ogg', '.aac', '.opus']:
        return 'Music'
    else:
        return 'Other'

def get_files(rc):
    todo = {}
    file_paths = []
    for subdir, dirs, files in os.walk(rc.original_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            file_category = get_file_category(file_path)

            if rc.condition_value == 'Extension':
                if rc.operator_value == 'is':
                    if file_path.endswith(rc.ext_value):
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)
                elif rc.operator_value == 'is not':
                    if file_path.endswith(rc.ext_value):
                        pass
                    else:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)

            elif rc.condition_value == 'Date Added':
                dt = datetime.datetime.strptime(rc.date_edit_value, '%Y-%m-%d')
                new_dt = int(dt.strftime('%Y%m%d'))
                file_date = int(datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y%m%d'))
                if rc.operator_value == 'is':
                    if new_dt == file_date:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)
                if rc.operator_value == 'is before':
                    if new_dt > file_date:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)
                if rc.operator_value == 'is after':
                    if new_dt < file_date:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)

            elif rc.condition_value == 'Size':
                global size_value
                size_value = float(size_value)
                if rc.operator_value == 'is':
                    size_of_file = human_size(os.path.getsize(file_path))
                    print("Calculated size of file: {}".format(size_of_file))
                    print("Size given in condition: {}".format(size_value))
                    if size_of_file == size_value == 0:
                        file_paths.append(file)
                    elif size_of_file == size_value:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)
                elif rc.operator_value == 'greater than':
                    size_of_file = human_size(os.path.getsize(file_path))
                    if size_of_file > size_value:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)
                elif rc.operator_value == 'less than':
                    size_of_file = human_size(os.path.getsize(file_path))
                    if size_of_file < size_value:
                        file_paths.append(file)
                        todo[file_path] = (rc.actions_value, file_category)

    return todo, file_paths


def run_task(rc, action_performed, file_to_process):  # file_to process == a
    if action_performed == 'Copy':
        actions.copy(file_to_process, rc.target_path)
    elif action_performed == 'Move':
        print(file_to_process)
        print(rc.target_path)
        actions.move(file_to_process, rc.target_path)
    elif action_performed == 'Delete':
        actions.delete(file_to_process)
    elif action_performed == 'Trash Bin':
        actions.trash_bin(file_to_process)
    elif action_performed == 'Rename':
        actions.rename(file_to_process, rc.rename_value)

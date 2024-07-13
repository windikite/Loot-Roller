import os, re, datetime, random

class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
 
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

def capitalizeFirstLetter(string):
    return string[0].upper() + string[1:]
    
def capitalizeWholeString(string):
    return string.upper()

def reverseIterable(iterable):
    return iterable[::-1]

def printCritical(text):
    print(colors.bg.black, colors.fg.red)
    print(text, colors.reset)

def printWarning(text):
    print(colors.bg.black, colors.fg.orange)
    print(text, colors.reset)

def printSuccess(text):
    print(colors.bg.black, colors.fg.green)
    print(text, colors.reset)

def printWorking(text):
    print(colors.bg.black, colors.fg.blue)
    print(text, colors.reset)

def askMenu(choices, text):
    counter = 1
    choice_list = []
    for choice in choices:
        new_choice = str(counter) + ". " + str(choice)
        choice_list.append(new_choice) 
        counter += 1
    separator = "\n"
    menu = separator.join(choice_list)
    printWorking(menu)
    printWarning(text)
    user_input = input("Selection: ")
    try:
        index = int(user_input)
        index <= len(choices) == True
        index >= 0 == True
    except ValueError:
        printCritical("Function error! Please make sure choose one of the chosen options!")
    except TypeError:
        printCritical("Function error! Please make sure to input numbers for menu selections!")
    else:
        return index-1
    
def backupFile(old_path):
    file_path = reverseIterable(reverseIterable(old_path)[0:reverseIterable(old_path).index("/")])
    dot_index = str(file_path).index(".")
    extension = file_path[dot_index:]
    file_name = file_path[:dot_index]
    path_to_save_to = f"./backups/{file_name}"
    # print(file_path, file_name, path_to_save_to, os.path.exists(path_to_save_to))
    if os.path.exists("./backups/") == False:
        os.mkdir("./backups/")
    if os.path.exists(path_to_save_to) == False:
        os.mkdir(path_to_save_to)
    try:
        if os.path.exists(old_path):
            if os.path.exists(path_to_save_to):
                now = datetime.datetime.now()
                new_path = path_to_save_to + "/" + file_name + str(now.year) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + extension
                os.rename(old_path, new_path)
            else:
                printCritical("Unable to backup!")
                return -1
        else:
            print("File to backup does not exist!")
            return 1
    except FileNotFoundError:
        printCritical("File not found!")
        return -2
    else:
        return 1    
    
def importToDict(path, fields):
    try:
        with open(path, "r") as file:
            open_file = file.read()
            lines = (str(open_file).strip()).split("\n")
            # print(open_file, lines)
            items = {}
            anti_overwrite_counter = 0#this is the best way I found to modify the id so that they wouldn't overwrite eachother, as I don't want to wait for a name field to come up for each line and then append that instead
            for line in lines:
                item = {}
                id = generateUniqueID(str(anti_overwrite_counter))
                anti_overwrite_counter += 1
                # print(id)
                for field in fields:
                    value = re.search(re.escape(field) + r"(\w*): ([A-Za-z0-9 @-]+([.][0-9]*)?|[.][0-9]+)", line)
                    if value != None:
                        value_index = str(value.group(0)).index(":")+2
                        value = str(value.group(0))[value_index:]
                        # print(value)
                        isFloat = re.search(r"^[0-9]+" + re.escape(".") + r"[0-9]+$", value)
                        isInt = re.search(r"^[0-9]+$", value)
                        value = float(value) if isFloat != None else value
                        value = int(value) if isInt != None else value
                        key_value = {field: value}
                        # print(value, type(value), isFloat, isInt)
                        item.update(key_value)
                        # print(str(value.group(0)), str(value.group(0))[split_value:])
                        # id = str(value.group(0))[split_value:] + 
                    else:
                        key_value = {field: "undefined"}
                        item.update(key_value)
                    # print(field, key_value)
                if len(item) >= 1:
                    # print("item", item)
                    items[id] = item
    except FileNotFoundError:
        printCritical("File not found!")
    # except Exception as e:
    #     print("Error!", e)
    else:
        return items

def writeStringsToFile(source, export_path, method):
    try:
        backup = backupFile(export_path)
        string_to_write = ("\n").join(source)
    except FileNotFoundError:
        printCritical("File not found!")
    except Exception as e:
        print("Error!", e)
    else:	
        if backup != -1:
            if string_to_write != -1:
                with open(export_path, method) as file:
                    file.write(string_to_write)
                printSuccess(f"Saved {export_path}!")
                return 1
            else:
                print("No string to write!")
        else:
            printCritical(f"Failed to backup previous file at {export_path} so prevented overwrite")
            return -1

def compileToString(source):
    try:
        strings = []
        if isinstance(source, dict):
            first_layer = source.values()
            for key_value in first_layer:
                second_layer = key_value.items()
                item = []
                for key, value in second_layer:
                    item.append(f"{key}: {value}")
                item = ", ".join(item)
                strings.append(item)
        elif isinstance(source, list):
            for item in source:
                parameter_list = []
                for parameter in item[1].items():
                    parameter_list.append(f"{parameter[0]}: {parameter[1]}")
                item = ", ".join(parameter_list)
                strings.append(item)
        else:
            printCritical("Unknown data type!")
        string_to_write = "\n".join(strings)
    except Exception as e:
        print("Error!", e)
    else:	
        if string_to_write != "":
            return string_to_write
        else:
            printCritical(f"Failed to compile data to writable string")
            return -1
        
def exportItemsToFile(source, export_path):
    try:
        backup = backupFile(export_path)
        string_to_write = compileToString(source)
    except FileNotFoundError:
        printCritical("File not found!")
    except Exception as e:
        print("Error!", e)
    else:	
        if backup != -1 and string_to_write != -1:
            with open(export_path, 'w') as file:
                file.write(string_to_write)
            printSuccess(f"Saved {export_path}!")
            return 1
        elif backup != -1 and string_to_write == -1:
            print()
        else:
            printCritical(f"Failed to backup previous file at {export_path} so prevented overwrite")
            return -1

def filterDict(old_dict, filter_key, filter_value, comparator):
    cleaned_dict = {key: old_dict[key] for key in dict(old_dict).keys() if "undefined" not in dict(old_dict[key]).values()}
    entries = cleaned_dict.items()
    filtered_dict = {}
    for entry_key, entry_value in entries:
        parameters = entry_value.items()
        for parameter in parameters:
            if comparator == "equal":
                if parameter[0] == filter_key and parameter[1] == filter_value:
                    filtered_dict.update({str(entry_key): entry_value})
            elif comparator == "less":
                if parameter[0] == filter_key and float(parameter[1]) <= float(filter_value):
                    filtered_dict.update({str(entry_key): entry_value})
            elif comparator == "greater":
                if parameter[0] == filter_key and float(parameter[1]) >= float(filter_value):
                    filtered_dict.update({str(entry_key): entry_value})
            else:
                print("Please use either less, equal or greater as a comparator!")
        # found_key_value = {k:v for (k, v) in old_dict.get(entry).items() if filter_key in k and filter_value in v}
        # print(found_key_value)
        # if found_key_value != "":
        #     filtered_dict[entry] = old_dict[entry]
    return filtered_dict

def createEntry(old_dict, fields):
    new_dict = old_dict
    new_entry = {}
    for field in fields:
        field_name = str(field[0])
        field_type = str(field[1])
        user_input = ""
        try:
            if field_type == "str":
                user_input = str(input(f"Please input {field_name} using alphanumeric characters: "))
            if field_type == "int":
                user_input = int(input(f"Please input {field_name} using numeric, non-decimal characters: "))
            if field_type == "float":
                user_input = float(input(f"Please input {field_name} using numeric characters (decimals are fine): "))
        except TypeError:
            print(f"That wasn't a {field_type}! Please retry!")
        else:
            new_entry.setdefault(field_name, user_input)
    new_dict[generateUniqueID()] = new_entry
    return new_dict

def deleteEntry(old_dict, entry):
    new_dict = old_dict.pop(entry)
    printSuccess("Deleted entry!")
    return new_dict

def searchEntry(source, fields):
    if source != {}:
        search_field = int(askMenu(fields, "Please choose the field you would like to search by: "))
        search_field = fields[search_field]
        search_term = str(input("Please input search term: "))
        filtered_list = list(filterDict(source, search_field, search_term, "equal").items())
        if len(filtered_list) > 1:
            chosen_index = int(askMenu(filtered_list, "Please choose an entry: "))
            chosen_entry = filtered_list[chosen_index]
            return chosen_entry
        if len(filtered_list) == 1:
            # returns as tuple
            return filtered_list[0]
        if len(filtered_list) <= 0:
            return -1
    else:
        return -1

def editEntry(old_dict, entry_id, fields):
    entry_to_edit = dict(old_dict).get(entry_id)
    field_to_change = int(askMenu(fields, "Please choose the field you would like to edit: "))
    field_to_change = fields[field_to_change]
    new_value = str(input(f"Please enter a new value for this entry's {field_to_change}: "))
    entry_to_edit[field_to_change] = new_value
    return old_dict

def displayEntries(source, text):
    entry_list = []
    string = ""
    source_dict = source
    if isinstance(source, tuple) == True:
        # print(dict.fromkeys(source[0], source[1]))
        temp_dict = {}
        temp_dict.update({source[0]: source[1]})
        source_dict = temp_dict
        # print("source dict", source_dict)
    if isinstance(source_dict, dict) == True:
        for entry in list(source_dict.items()):
            field_list = []
            field_list.append(f"ID: {entry[0]}")
            for field in entry[1].items():
                field_list.append(str(f"{str(field[0]).upper()}: {field[1]}"))
            separator = " | "
            entry_list.append(separator.join(field_list)) 
    if isinstance(source, list) == True:
        for entry in source_dict:
            field_list = []
            field_list.append(f"ID: {entry[0]}")
            for field in entry[1].items():
                field_list.append(str(f"{str(field[0]).upper()}: {field[1]}"))
            separator = " | "
            entry_list.append(separator.join(field_list)) 
    if len(entry_list) >= 1:
        separator = "\n"
        string = separator.join(entry_list)
    else:
        string = "None found!"
    printSuccess(text)
    printWorking(string)
    
def generateUniqueID(prefix=False):
    if prefix != False:
        string = str(prefix) + str(datetime.datetime.now().microsecond)
        return str(string)
    else:
        return str(datetime.datetime.now().microsecond)
    

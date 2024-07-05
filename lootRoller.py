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

def scanDirectory(path, term):
    dir = os.read(path)
    return dir

def filterDirectory(dir, term):
    pass

def backupFile(path):
    index = path.index(".")
    extension = path[index:]
    file_name = path[:index]
    path_to_save = f"./backups/{file_name}"
    old_path = f"./tables/{file_name}{extension}"
    if os.path.exists("./backups/") == False:
        os.mkdir("./backups/")
    if os.path.exists(path_to_save) == False:
        os.mkdir(path_to_save)
    try:
        if os.path.exists(path_to_save) and os.path.exists(old_path):
            now = datetime.datetime.now()
            new_path = path_to_save + "/" + file_name + str(now.year) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + extension
            os.rename(old_path, new_path)
        else:
            printCritical("Unable to backup!")
            return -1
    except FileNotFoundError:
        printCritical("File not found!")
        return -1
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
                id = str(datetime.datetime.now().microsecond) + str(anti_overwrite_counter)
                anti_overwrite_counter += 1
                # print(id)
                for field in fields:
                    value = re.search(re.escape(field) + r"(\w*): [A-Za-z0-9 ]+", line)
                    if value != None:
                        split_value = str(value.group(0)).index(":")+2
                        key_value = {field: str(value.group(0))[split_value:]}
                        # print(value)
                        # print(split_value, key_value, value)
                        item.update(key_value)
                        # print(str(value.group(0)), str(value.group(0))[split_value:])
                        # id = str(value.group(0))[split_value:] + 
                    else:
                        pass
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

def exportItemsToFile(source, name):
    try:
        backup = backupFile(name)
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
        string_to_write = "\n".join(strings)
    except FileNotFoundError:
        printCritical("File not found!")
    # except Exception as e:
    #     print("Error!", e)
    else:	
        table_path = "./tables/" + name
        if backup != -1:
            with open(table_path, 'w') as file:
                file.write(string_to_write)
            printSuccess(f"Saved {table_path}!")
            return 1
        else:
            printCritical(f"Failed to backup previous file at {table_path} so prevented overwrite")
            return -1
        

def appendItemToFile():
    pass

def rollRandom(source, number):
    all_items = source.items()
    # print("all items", all_items)
    rolled = []
    while len(rolled) < number:
        rolled_number = random.randrange(0, len(all_items)-1)
        for index, value in enumerate(all_items):
            if index == rolled_number:
                rolled.append(value)
                # print(f"Rolled a {value}!")
            else:
                printCritical("Roll was out of bounds!")
    if len(rolled) == number:
        printSuccess(f"Rolled all items!")
        return rolled
    elif len(rolled) > 0:
        printWarning("Failed to roll all items!")
        return rolled
    else:
        printCritical("Failed to roll any items...")
        return None
    
def rollValue(source, target_value):
    current_value = 0.0
    floored_items = filterDict(source, "cost", target_value*0.3, "greater")
    filtered_items = filterDict(floored_items, "cost", target_value*1.3, "less").items()
    rolled = []
    while current_value < target_value and len(filtered_items) > 1:
        rolled_number = random.randrange(0, len(filtered_items)-1) if len(filtered_items) > 0 else None
        if rolled_number != None:
            for index, value in enumerate(filtered_items):
                if index == rolled_number:
                    rolled.append(value)
                    current_value = current_value + float(dict(value[1])["cost"])
                    floored_items = filterDict(source, "cost", (target_value-current_value)*0.3, "greater")
                    filtered_items = filterDict(floored_items, "cost", (target_value-current_value)*1.3, "less").items()
    if len(rolled) >= 0:
        printSuccess(f"Rolled items worth {current_value}!")
        return rolled
    else:
        printCritical("Failed to roll any items...")
        return None

def filterDict(old_dict, filter_key, filter_value, comparator):
    # print(old_dict)
    entries = old_dict.items()
    # print(entries)
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
        # found_key_value = {k:v for (k, v) in old_dict.get(entry).items() if filter_key in k and filter_value in v}
        # print(found_key_value)
        # if found_key_value != "":
        #     filtered_dict[entry] = old_dict[entry]
    return filtered_dict

def createItem(old_dict):
    new_dict = old_dict
    item_name = str(input("Please input an item name: "))
    item_cost = float(input("Please input the item's cost in gold: "))
    item_type = str(input("Please input the item's type: "))
    created_item = {"name": item_name, "cost": item_cost, "type": item_type}
    new_dict[str(datetime.datetime.now().microsecond)] = created_item
    return new_dict

equipment = importToDict("./tables/equipment.txt", ["name", "cost", "type"])
# print(equipment)
terrain = importToDict("./tables/terrain.txt", ["name", "description"])
wondrous_items = filterDict(equipment, "type", "wondrous", "equal")
print("here is a list of all wondrous items: ", wondrous_items)
print("here is a list of all armor: ", filterDict(equipment, "type", "armor", "equal"))
# rollRandom(equipment, 4)
# equipment = createItem(equipment)

# exportItemsToFile(equipment, "equipment.txt")
# exportItemsToFile(terrain, "terrain.txt")
# exportItemsToFile(rollRandom(equipment, 4), "loot.txt")
# print(rollValue(equipment, 5000))
# print(rollValue(equipment, 4000))
exportItemsToFile(rollValue(equipment, 12000), "loot.txt")
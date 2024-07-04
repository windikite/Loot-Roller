import os, re, datetime, random

def scanDirectory(path, term):
    dir = os.read(path)
    return dir

def filterDirectory(dir, term):
    pass

def backupFile(path):
    print("path", path)
    index = path.index(".")
    extension = path[index:]
    file_name = path[:index]
    path_to_save = "./backups/" + file_name
    old_path = "./tables/" + file_name
    if os.path.exists(path_to_save) == False:
        os.mkdir(path_to_save)
    try:
        if os.path.exists(path_to_save) and os.path.exists(old_path):
            now = datetime.datetime.now()
            new_path = path_to_save + "/" + file_name + str(now.year) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + extension
            print("new path", new_path)
            os.rename(old_path, new_path)
    except FileNotFoundError:
        print("File not found!")
        return -1
    else:
        return 1


def importToDict(path, fields):
    print(path)
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
        print("File not found!")
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
        print("File not found!")
    # except Exception as e:
    #     print("Error!", e)
    else:	
        table_path = "./tables/" + name
        if backup != -1:
            with open(table_path, 'w') as file:
                file.write(string_to_write)
            print(f"Saved {table_path}!")
            return 1
        else:
            print(f"Failed to backup previous file at {table_path} so prevented overwrite")
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
    if len(rolled) == number:
        print(f"Rolled all items!")
        return rolled
    elif len(rolled) > 0:
        print("Failed to roll all items!")
        return rolled
    else:
        print("Failed to roll any items...")
        return None

def filterDict(old_dict, filter_key, filter_value):
    # print(old_dict)
    entries = old_dict.items()
    # print(entries)
    filtered_dict = {}
    for entry_key, entry_value in entries:
        parameters = entry_value.items()
        for parameter in parameters:
            if parameter[0] == filter_key and parameter[1] == filter_value:
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
held_items = filterDict(equipment, "type", "held")
print("here is a list of all held items: ", held_items)
print("here is a list of all armor: ", filterDict(equipment, "type", "armor"))
rollRandom(equipment, 2)
# equipment = createItem(equipment)

exportItemsToFile(equipment, "equipment.txt")
exportItemsToFile(terrain, "terrain.txt")
exportItemsToFile(rollRandom(equipment, 3), "loot.txt")

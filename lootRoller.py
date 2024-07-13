import random
from functions import *

class horde:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.totalValue = 0
        self.hordeType = ""
        
    def generateHorde(self, source, loot_profile, target_value):
        self.hordeType = loot_profile
        horde = rollHorde(source, self.hordeType, target_value)
        if horde != None:
            self.items = [item for item in horde]
            self.items.sort()
            self.totalValue = 0
            for item in self.items:
                self.totalValue = self.totalValue + item[1].get("cost") 
            # print(f"Rolled {len(self.items)} items worth {self.totalValue}")
        else:
            print("Failed to generate horde")
        
    def info(self):
        hordeName = self.hordeType.get("name")
        displayEntries(self.items, f"This {hordeName} horde has {len(self.items)} items in it worth a total of {self.totalValue}g.")

def printHordes(hordes):
    for horde in hordes.items():
        horde[1].info()
        
def createHordes(source, loot_profiles, number):
    print(loot_profiles.items())
    counter = 0
    hordes = {}
    while counter < number:
        mode = int(askMenu([loot_profiles[profile]["name"] for profile in loot_profiles], "Please choose a horde type: "))
        target_value = int(input("Please enter a target value for the horde: "))
        new_horde = horde(generateUniqueID("horde"))
        new_horde.generateHorde(source, list(loot_profiles.items())[mode][1], target_value)
        hordes.update({new_horde.id: new_horde})
        counter += 1
    if len(hordes.items()) > 0:
        return hordes
    else:
        return -1

def exportHordesToFile(hordes, export_path):
    stringList = []
    counter = 0
    for horde in hordes.items():
        horde_title = "Horde " + str(counter+1)
        stringList.append(f"{horde_title}: A {horde[1].hordeType.get("name")} worth {horde[1].totalValue}")
        for item in horde[1].items:
            stringList.append(f"{item[1].get("name")} - {item[1].get("cost")}")
        stringList.append("-------------")
        counter += 1
    print(stringList)
    writeStringsToFile(stringList, export_path, "w")

def rollSetNumberOfLoot(source, number):
    all_items = source.items()
    # print("all items", all_items)
    rolled = []
    while len(rolled) < number and len(all_items) > 0:
        rolled_number = random.randint(1, len(all_items)) if len(all_items) > 0 else None
        if type(rolled_number) == int:
            for index, value in enumerate(all_items):
                if index == rolled_number-1:
                    rolled.append(value)
                    # print(f"Rolled a {value}!")
        else:
            print("Rolled type is not number!")
    if len(rolled) == number:
        printSuccess(f"Rolled all items!")
        return rolled
    elif len(rolled) > 0:
        printWarning("Failed to roll all items!")
        return rolled
    else:
        printCritical("Failed to roll any items...")
        return None
    
def rollTargetLootValue(source, target_value, mode):
    min_value = target_value*.2
    max_value = target_value*.8
    current_value = 0.0
    if mode == "more":
        min_value = target_value*.2
        max_value = target_value*.8
    elif mode == "fewer":
        min_value = target_value*.5
        max_value = target_value*.9
    elif mode == "least":
        min_value = target_value*.7
        max_value = target_value*1.1
    rolled = []
    floored_items = filterDict(source, "cost", min_value, "greater")
    filtered_items = filterDict(floored_items, "cost", max_value, "less").items()
    failed_attemps = 0
    while current_value < target_value and failed_attemps < 10:
        if len(filtered_items) > 1:
            rolled_number = random.randint(1, len(filtered_items))
            if type(rolled_number) == int:
                for index, value in enumerate(filtered_items):
                    if index == rolled_number-1:
                        rolled.append(value)
                        current_value = current_value + float(dict(value[1])["cost"])
                        min_value = min_value*.8
                        max_value = max_value*.8
                        floored_items = filterDict(source, "cost", min_value, "greater")
                        filtered_items = filterDict(floored_items, "cost", max_value, "less").items()
                        failed_attemps = 0
        elif len(filtered_items) == 1:
            rolled.append(list(filtered_items)[0])
            min_value = min_value*.5
            max_value = max_value*.8
            floored_items = filterDict(source, "cost", min_value, "greater")
            filtered_items = filterDict(floored_items, "cost", max_value, "less").items()
            failed_attemps = 0
        else:
            min_value = min_value*.25
            max_value = max_value*.9
            floored_items = filterDict(source, "cost", min_value, "greater")
            filtered_items = filterDict(floored_items, "cost", max_value, "less").items()
        failed_attemps += 1
    if len(rolled) > 0:
        # printSuccess(f"{len(rolled)} rolled items worth {current_value}!")
        return rolled
    else:
        printCritical("Failed to roll any items...")
        return None

def rollHorde(source, horde_type, target_value):
    horde_name = horde_type.get("name")
    horde_modifier = horde_type.get("loot_value_multiplier")
    horde_quantity = horde_type.get("loot_quantity")
    horde_value = float(target_value)*float(horde_modifier)
    # print(target_value, horde_modifier, horde_value)
    possible_loot = source
    if possible_loot != -1:
        loot_horde = rollTargetLootValue(filterDict(possible_loot, "cost", horde_value, "less"), horde_value, horde_quantity)
        if loot_horde != -1:
            # print(f"Attempted to roll a {horde_name} worth {horde_value}g! Rolled the following items: \n{loot_horde}")
            return loot_horde
        else:
            print(f"Attempted to roll a {horde_name} worth {horde_value}g! There were no items with that search criteria to roll for.")
            return -1
    elif possible_loot == -1:
        print(f"Attempted to roll a {horde_name} worth {horde_value}g! There were no items with that search criteria to roll for.")
        return -1
    print("--------------")

def mainLoop():
    # backup management
    backup_location = "./backups"
    # loot management
    loot_file_location = "./loot.txt"
    # equipment management
    equipment_file_location = "./tables/equipment.txt"
    equipment_fields = ["name", "type", "cost"]
    equipment = importToDict(equipment_file_location, equipment_fields)
    # material management
    material_file_location = "./tables/craftingMaterials.txt"
    material_fields = ["name", "cost", "type", "weight"]
    craftingMaterials = importToDict(material_file_location, material_fields)
    # loot profiles for horde generation managment
    loot_profile_fields = ["name", "loot_value_multiplier", "loot_quantity"]
    loot_profiles = importToDict("./lootProfiles.txt", loot_profile_fields)
    while True:
        user_input = askMenu([
                "Create new item", 
                "Edit an item", 
                "Delete an item", 
                "Search for an item", 
                "Display all items", 
                "Roll loot",
                "Export item database to a text file", 
                "Import item database from a text tile", 
                "Quit"], 
                "Please choose an operation: ")
        try:
            user_input = int(user_input)
            id_to_edit = ""
            if user_input == 0:
                equipment = createEntry(equipment, [("name", "str"), ("cost", "float"), ("type", "str")])
            elif user_input == 1:
                search_method = int(askMenu(["Edit from full list", "Search for contact to edit"], "Please choose an operation: "))
                id_to_edit = ""
                if search_method == 0:
                    list_of_equipment = equipment.items()
                    index_to_edit = int(askMenu(list_of_equipment, "Please choose one to edit: "))
                    id_to_edit = list(list_of_equipment)[index_to_edit][0]
                elif search_method == 1:
                    if equipment != {}:
                        id_to_edit = searchEntry(equipment, equipment_fields)[0]
                if id_to_edit != "" and id_to_edit != -1:
                    editEntry(equipment, id_to_edit, equipment_fields)
                else:
                    print("Unable to find an entry to edit!")
            elif user_input == 2:
                search_method = int(askMenu(["Delete from full list", "Search for an item to delete"], "Please choose an operation: "))
                id_to_delete = ""
                if search_method == 0:
                    list_of_equipment = equipment.items()
                    index_to_delete = int(askMenu(list_of_equipment, "Please choose one to delete: "))
                    id_to_delete = list(list_of_equipment)[index_to_delete][0]
                elif search_method == 1:
                    if equipment != {}:
                        id_to_delete = searchEntry(equipment, equipment_fields)[0]
                if id_to_delete != "" and id_to_delete != -1:
                    deleteEntry(equipment, id_to_delete)
                else:
                    print("Unable to find an entry to delete!")
            elif user_input == 3:
                entry = searchEntry(equipment, equipment_fields)
                displayEntries(entry, "Item Info: ")
            elif user_input == 4:
                displayEntries(equipment, "equipment: ")
            elif user_input == 5:
                user_input = int(askMenu(["Roll random loot", "Roll a target value", "Roll loot horde"], "Please choose an option: "))
                if user_input == 0:
                    target_number = int(input("Please input a number of items to roll: "))
                    horde = rollSetNumberOfLoot(equipment | craftingMaterials, target_number)
                    user_input = int(askMenu(["Yes", "No"], "Export to file? : "))
                    if user_input == 0:
                        exportItemsToFile(horde, loot_file_location)
                    elif user_input == 1:
                        printWorking("Returning to menu...")
                elif user_input == 1:
                    target_value = float(input("Please input a target value in gold: "))
                    mode = int(askMenu(["More items to reach target", "Fewer items to reach target", "Least items to reach target"], "Please choose an option: "))
                    horde = rollTargetLootValue(equipment | craftingMaterials, target_value, mode)
                    user_input = int(askMenu(["Yes", "No"], "Export to file? : "))
                    if user_input == 0:
                        exportItemsToFile(horde, loot_file_location)
                    elif user_input == 1:
                        printWorking("Returning to menu...")
                elif user_input == 2:
                    number = int(input("How many hordes do you want to roll?: "))
                    hordes = createHordes(equipment, loot_profiles, number)
                    printHordes(hordes)
                    user_input = int(askMenu(["Yes", "No"], "Export to file? : "))
                    if user_input == 0:
                        exportHordesToFile(hordes, loot_file_location)
                    elif user_input == 1:
                        printWorking("Returning to menu...")
            elif user_input == 6:
                exportItemsToFile(equipment, "./tables/equipment.txt")
            elif user_input == 7:
                equipment = importToDict(equipment_file_location, equipment_fields)
            elif user_input == 8:
                break
        except Exception as e:
            printCritical(e)
        else:
            printSuccess("Done!")


mainLoop()
from pathlib import Path


class Character:
    name = ""
    class_name = ""
    race = ""
    hp = 0
    attack = 0
    special_attack = 0
    defence = 0
    weapon_attack = 0
    armor_defence = 0
    mana = 0
    stamina = 0
    level = 0
    ally = False

    def __init__(characterDict):
        pass


def getStatsFromFileText(aFileTextLines):
    charDict = {}
    for line in aFileTextLines:
        (prop, value) = line.split(':')
        prop = prop.strip()
        value = value.strip()
        charDict[prop] = value
    return charDict

dir_path = Path (".")
for entry in dir_path.iterdir():
    if entry.suffix == ".txt": # only process .txt files
     with open(entry, 'r') as file:
        print(f"Reading {entry.name}\n")
        lines = file.readlines()
        charDict = getStatsFromFileText(lines)
        print(lines)
        print("\n")


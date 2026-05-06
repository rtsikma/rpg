from pathlib import Path
from enum import Enum

class BattleResult(Enum):
    AllyWins = 1
    EnemyWins = 2
    BothLose = 3


# Lists of characters
allyList = []
enemyList = []

class Character:
    def __init__(self, characterDict):
        self.name = characterDict['Name']
        self.class_name = characterDict['Class']
        self.race = characterDict['Race']
        self.hp = characterDict['HP']
        self.attack = characterDict['Attack']
        self.special_attack = characterDict['Special_Attack']
        self.defence = characterDict['Defense']
        self.weapon_attack = characterDict['Weapon_Attack']
        self.armor_defence = characterDict['Armor_Defense']
        self.mana = characterDict['Mana']
        self.stamina = characterDict['Stamina']
        self.level = characterDict['Level']
        self.ally = characterDict['Ally']

    def isAlive(self):
        return self.hp > 0

    def takeTurn(self, battle):
        # select move (attack, heal)
        # select (enemy, ally)
        # if attack, roll 0 to (Attack + 1) for attack
        # and select enemy to attack

        # if heal, roll 0 to Special_attack for healing amount
        # and select ally to heal
        pass

class RpgBattle:
    def __init__(self, allies, enemies):
        self.allies = allies
        self.enemies = enemies

    def battle(self):
        # while both teams have characters alive
        while len(self.ally) > 0 and len(self.enemies) > 0:
            for ally in self.allies:
                if ally.isAlive():
                    ally.takeTurn(self.enemies)
                
            # do a turn for each ally
            # do a turn for each enemy
            # check if a team wins after each turn

        return BattleResult.BothLose


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


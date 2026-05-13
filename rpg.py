from pathlib import Path
from enum import Enum
import math
import random

class BattleResult(Enum):
    AllyWins = 1
    EnemyWins = 2
    BothLose = 3


# Lists of characters
allyList = []
enemyList = []

class RpgBattle:
    def __init__(self, allies, enemies):
        self.allies: list = allies
        self.enemies: list = enemies

    def allAlliesDead(self) -> bool:
        for ally in self.allies:
            if ally.isAlive():
                return False
        return True

    def allEnemiesDead(self) -> bool:
        for foe in self.enemies:
            if foe.isAlive():
                return False
        return True

    def battle(self) -> BattleResult:
        # while both teams have characters alive
        while not self.allAlliesDead() or not self.allEnemiesDead():
            for ally in self.allies:
                if ally.isAlive():
                    ally.takeTurn(self)
            
            for foe in self.enemies:
                if foe.isAlive():
                    foe.takeTurn(self)
        
        allEnemiesDead = self.allEnemiesDead()
        allAlliesDead = self.allAlliesDead()
        if allEnemiesDead and allAlliesDead:
            return BattleResult.BothLose
        elif allEnemiesDead:
            return BattleResult.AllyWins
        else:
            return BattleResult.EnemyWins


class Character:
    def __init__(self,
                 characterDict: dict
                ):
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
    
    def battle(self, foe):
        # Attack Algorithm
        # Roll for attack value
        # Roll for defense value
        # attack * weapon / armor - defense 

        # if attack, roll 0 to (Attack + 1) for attack (attack + 1 is critical hit)
        attackRoll = random.randint(0, self.attack + 1)
        if attackRoll == self.attack + 1:
            attackRoll = int(attackRoll * 1.5)
        defenseRoll = random.randint(0, foe.defence)
        attack = attackRoll * self.weapon_attack / foe.armor_defense - defenseRoll
        foe.hp -= math.max(attack, 0)

    def takeTurn(self, battle: RpgBattle):
        if self.ally:
            x = input("Attack (1) or Heal (2): ")
            if x == 1: # Attack
                foe = None
                for foe1 in battle.enemies:
                    if foe1.isAlive():
                        foe = foe1
                if foe != None:
                    self.battle(foe)
            if x == 2: # Heal        
                pass
        else:
            pass
        # select move (attack, heal)
        # select (enemy, ally)
        # if attack, roll 0 to (Attack + 1) for attack
        # and select enemy to attack

        # if heal, roll 0 to Special_attack for healing amount
        # and select ally to heal
        pass


def getStatsFromFileText(aFileTextLines: list):
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


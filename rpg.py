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
        self.max_hp = self.hp
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
    
    def attack(self, target):
        # if attack, roll 0 to (Attack + 1) for attack (attack + 1 is critical hit)
        attackRoll = random.randint(0, self.attack + 1)
        # This is a Critical Hit!
        if attackRoll == self.attack + 1:
            attackRoll = int(attackRoll * 1.5)
        defenseRoll = random.randint(0, target.defence)
        attackValue = attackRoll * self.weapon_attack / target.armor_defense - defenseRoll
        target.hp = max(target.hp - attackValue, 0)
        print(f"{self.name} ATTACKS {target.name} for {attackValue} HP. {target.name} now has {target.hp} HP.")

    def heal(self, target):
        heal_amount = random.randint(0, self.special_attack)
        target.hp = min(target.hp + heal_amount, target.max_hp)
        print(f"{self.name} HEALS {target.name} for {heal_amount} HP. {target.name} now has {target.hp} HP.")

    def findWeakestCharacter(self, charList: list):
        targets = [character for character in charList if character.isAlive()]
        if not targets:
            return ()
        target = min(targets, key=lambda c: c.hp)
        return target

    def takeTurn(self, battle: RpgBattle):
        if self.ally:
            x = input("Attack (1) or Heal (2): ")
            if x == 1: # Attack
                target = self.findWeakestCharacter(battle.enemies)
                if not target:
                    return
                self.attack(target)
            if x == 2: # Heal        
                target = self.findWeakestCharacter(battle.allies)
                if not target:
                    return
                self.heal(target)
        else:
            target = self.findWeakestCharacter(battle.allies)
            if not target:
                return
            self.attack(target)


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


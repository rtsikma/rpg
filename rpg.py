from pathlib import Path
from enum import Enum
import math
import random

XP_TO_LEVEL_UP = 3
DEBUG = True

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
    
    def earn_xp(self, xp_to_add: int):
        for ally in self.allies:
            ally.add_xp(xp_to_add)

    def battle(self) -> BattleResult:
        # while both teams have characters alive
        while not self.allAlliesDead() and not self.allEnemiesDead():
            for ally in self.allies:
                if ally.isAlive():
                    ally.takeTurn(self)
            
            for foe in self.enemies:
                if foe.isAlive():
                    foe.takeTurn(self)
        
        print("BATTLE IS OVER!")
        allEnemiesDead = self.allEnemiesDead()
        allAlliesDead = self.allAlliesDead()
        if allEnemiesDead and allAlliesDead:
            return BattleResult.BothLose
        elif allEnemiesDead:
            # add XP here!
            self.earn_xp(1)
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
        self.hp = int(characterDict['Hp'])
        self.max_hp = self.hp
        self.attack_value = int(characterDict['Attack'])
        self.special_attack = int(characterDict['Special_Attack'])
        self.defence = int(characterDict['Defence'])
        self.weapon_attack = int(characterDict['Weapon_Attack'])
        self.armor_defence = int(characterDict['Armor_Defence'])
        self.mana = int(characterDict['Mana'])
        self.stamina = int(characterDict['Stamina'])
        self.level = int(characterDict['Level'])
        self.ally = characterDict['Ally'] == "True"
        self.xp = 0
        self.xp_to_level_up = XP_TO_LEVEL_UP # amount of XP needed to get to next level

    def __str__(self):
        return (
        f"Name: {self.name}\n"
        f"Class: {self.class_name}\n"
        f"Race: {self.race}\n"
        f"HP: {self.hp}\n"
        f"Attack: {self.attack_value}\n"
        f"Special Attack: {self.special_attack}\n"
        f"Defence: {self.defence}\n"
        f"Weapon Attack: {self.weapon_attack}\n"
        f"Armor Defence: {self.armor_defence}\n"
        f"Mana: {self.mana}\n"
        f"Stamina: {self.stamina}\n"
        f"Level: {self.level}\n"
        f"Ally: {self.ally}\n"
        f"XP: {self.xp}\n"
        f"XP to Level Up: {self.xp_to_level_up}\n"
        )
    
    def isAlive(self):
        return self.hp > 0
    
    def attack(self, target):
        # if attack, roll 0 to (Attack + 1) for attack (attack + 1 is critical hit)
        attackRoll = random.randint(0, self.attack_value + 1)
        # This is a Critical Hit!
        if attackRoll == self.attack_value + 1:
            attackRoll = int(attackRoll * 1.5)
        defenceRoll = random.randint(0, target.defence)
        attackValue = max(0, int(attackRoll * self.weapon_attack / target.armor_defence - defenceRoll))
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
            x = int(input("Attack (1) or Heal (2): "))
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

    def increase_stats(self, value_to_increase: int):
        self.max_hp += value_to_increase
        self.hp += value_to_increase
        self.attack_value += value_to_increase
        self.special_attack += value_to_increase
        self.defence += value_to_increase
        self.weapon_attack += value_to_increase
        self.armor_defence += value_to_increase
        self.mana += value_to_increase
        self.stamina += value_to_increase

    def level_up(self):
        self.level += 1
        self.increase_stats(1)
        self.xp_to_level_up += XP_TO_LEVEL_UP

        print(f"{self.name} has levelled up to {self.level}.\n")
        print(self)

    def add_xp(self, xp_to_add):
        self.xp += xp_to_add
        if self.xp >= self.xp_to_level_up:
            self.level_up()


def getStatsFromFileText(aFileTextLines: list):
    charDict = {}
    for line in aFileTextLines:
        (prop, value) = line.split(':')
        prop = prop.strip()
        value = value.strip()
        charDict[prop] = value
    return charDict

def loadAllCharacters(path: str):
    dir_path = Path (path)
    for entry in dir_path.iterdir():
        if entry.suffix == ".txt": # only process .txt files
            file = open(entry, 'r')
            if DEBUG:
                print(f"Reading {entry.name}\n")
            lines = file.readlines()
            charDict = getStatsFromFileText(lines)
            char = Character(charDict)
            if char.ally:
                allyList.append(char)
            else:
                enemyList.append(char)
    if DEBUG:
        print("Ally List:\n")
        for ally in allyList:
            print(ally)
        print("\n\n\nEnemy List:\n")
        for enemy in enemyList:
            print(enemy)
            

def main():
    loadAllCharacters(".")
    battle = RpgBattle(allyList, enemyList[3:5])
    battle.battle()

if __name__ == '__main__':
    main()
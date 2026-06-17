from pathlib import Path
from enum import Enum
import copy
import random

XP_TO_LEVEL_UP = 3
DEBUG = False

class BattleResult(Enum):
    AllyWins = 1
    EnemyWins = 2
    BothLose = 3


# Lists of characters
allyList = []
enemyList = []
enemyListL2 = []

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
        
        print("The battle is over.\n")
        allEnemiesDead = self.allEnemiesDead()
        allAlliesDead = self.allAlliesDead()
        if allEnemiesDead and allAlliesDead:
            return BattleResult.BothLose
        elif allEnemiesDead:
            # add XP here!
            self.earn_xp(1)
            print("Link and Noragami are victorious!\n")
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
    
    def findWeakestForHealing(self, charList: list):
        target = min(charList, key=lambda c: c.hp)
        return target

    def takeTurn(self, battle: RpgBattle):
        if self.ally:
            strX = input(f"{self.name}: Attack (1) or Heal (2): ")
            if (strX == ""):
                print("Invalid Input\n")
                strX = input(f"{self.name}: Attack (1) or Heal (2): ")
            x = int(strX)
            if x == 1: # Attack
                target = self.findWeakestCharacter(battle.enemies)
                if not target:
                    return
                self.attack(target)
            if x == 2: # Heal        
                target = self.findWeakestForHealing(battle.allies)
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
        self.hp = self.max_hp
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
                if char.level > 1:
                    enemyListL2.append(char)
                else:
                    enemyList.append(char)
    if DEBUG:
        print("Ally List:\n")
        for ally in allyList:
            print(ally)
        print("\n\n\nEnemy List:\n")
        for enemy in enemyList:
            print(enemy)

class StoryItem:
    def __init__(self, description:str, enemies:int, level=1):
        self.description = description
        self.enemies = enemies
        self.enemy_level = level
    
    def showStory(self):
        print(self.description)
        if self.enemy_level == 1:
            enemies = copy.deepcopy(enemyList[0:self.enemies])
        else:
            enemies = enemyListL2
        if len(enemies) > 0:
            battle = RpgBattle(allyList, enemies)
            result = battle.battle()
            input("Press Enter to continue")
            return result
        
        return BattleResult.AllyWins

def createStory():
    desc1 = """
Link and Noragami are aimlessly walking along in a dangerous and spooky woods.
They are discussing deep and serious matters (for teenagers).
Suddenly they are attacked by a mysterious enemy.
"""
    desc2 = """
After successfully defeating their attacker, Link and Noragami continue to wander aimlessly.
They continue their deep and serious discussion (for teenagers).
Their discussions include what they would do if they won the lottery, and plans for world domination.
Just when they were finalizing their plans, 2 enemies confronted them.
"""
    desc3 = """
With their attackers now lying in pools of their own blood, Link and Noragami continue their aimless wanderings.
Due to the stress of their battle, they have forgotten all of their world domination plans, and must begin again.
The new plans are even better than their first ones. They were just discussing how to properly buy the lottery, when they again were attacked by 2 enemies.
"""
    desc4 = """
Now that the attackers were vanquished by the skilled warriors, Link and Noragami again resumed their world domination plans. Unfortunately, they have forgotten their world domination plans again.
Thus, they decided that they should first figure out how to get rich, then work on the world domination plans, since they would need lots of money to implement any plans they would inevitably come up with.
They were coming into a clearing just as they were finalizing their get-rich schemes. As they entered the clearing, 3 enemies jumped out from behind a rock to attack them.
"""
    desc5 = """
Even though they conquered their foes, Link and Noragami again forgot all of their plans.
They continued their fooling aimless wandering deeper into the dangerous and spooky woods.
Just as they were again finalizing they improved get-rich schemes, they were again ambushed by a group of enemies
"""
    desc6 = """
After the battle finished, Link and Noragami realized that their plans were all forgotten again. They decided to write their plans down, so they wouldn't forgot them.
Because they had done this several times already, the plans Link and Noragami came up with this time were better than ever - fool-proof, even. With their plans written down, they moved confidently forward.
As they moved along the path, 4 enemies jumped out of the woods and began to attack them.
"""
    desc7 = """
After the long, gruelling battle, Link and Noragami again forgot all of the plans they made. Unfortunately, their written plans were dropped during the battle. Despite being attacked 6 times, the 2 friends continued walking deeper into the dark and spooky woods.
Since they had forgotten all of their previous plans, they decided to move on from world domination plans and get-rich schemes to Link's new computer that he is hoping to build.
After several minutes of discussing the desired specs, they suddenly felt an overpowering sense of dread. They had come to the center of the forest. In front of them was a huge menacing figure.
"You have defeated all my underlings!", the figure said, "Now I will have to take care you my self!"
"""
    desc8 = """
After defeating the huge warrior, Link and Noragami decided that the dark and spooky forest was no place them.
They quickly retraced their steps out of the forest, completely forgetting about their plans for world domination and get-rich schemes that were dropped on the forest floor. Link and Noragami decided to go to Link's house to play Pokemon.
"""
    storyList = (
        StoryItem(desc1, 1),
        StoryItem(desc2, 2),
        StoryItem(desc3, 2),
        StoryItem(desc4, 2),
        StoryItem(desc5, 3),
        StoryItem(desc6, 4),
        StoryItem(desc7, 1, 2),
        StoryItem(desc8, 0)
    )

    for story in storyList:
        result = story.showStory()
        if result == BattleResult.EnemyWins:
            print("\n\nLink and Noragami perished while aimlessly wandering around a dark and spooky forest")
            break

def main():
    loadAllCharacters(".")
    createStory()

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Plate Tectionics Killed JFK

Originally conceived summer 2017

By Jake Roush and Brennan McClurg

Last updated 5/4/18
"""

#%%
import numpy as np
import pandas as pd
import collections

import warnings # Ignoring depreciated warnings coming from python
def fxn():
    warnings.warn("deprecated", DeprecationWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

# Disabling false positive warning message that appears in the battle function
pd.options.mode.chained_assignment = None  # default='warn'

'''
##### THINGS TO DO ######
Write a function for calculating damage dealt - DONE
Create a dataframe with character stats - DONE
Create a dataframe with monster stats - DONE
Create a dataframe with item (weapon) stats - DONE
Make items and add to battle function - DONE
Also fix character dying at end of winning battle? -- Convert dataframe index return values to int - DONE
Use keystroke module to pace dialogue by only allowing user to proceed by pressing enter. To keep immersion, we want to prevent them from being able to type anything.
Implement XP and money systems - gives incentive for fighting monsters - DONE (but nothing to spend it on yet!)
Create a town to return to after fighting and running away
    Have options for:
        sleeping - DONE
        buying/selling
        random monster encounter - DONE
        moving to different town
Find a way to easily return multiple values from battle function and assign to character dataframe - DONE
    Return a tuple with everything that has changed in the battle
        Health
        Exp (not in yet)
        Gold (not in yet)
        Number of items (hp/mana potions)
        Item drops (weapons, armor, etc)
    Need to find a way to create a list/tuple like object that links directly to 
    the characterStats dataframe - want it to contain the actual values inside the dataframe,
    NOT just it's value
    USE A FOR LOOP
Create GUI - pokemon battle style?
     
'''
        
        
# Creating named tuple of all variables changed by the result of battling
normalbattlereturn = collections.namedtuple('normalbattlereturn',['hp','exp','gold','healthpots','manapots'])
# Example of what returning this tuple in a battle would look like:
#batresult = normalbattlereturn(hp=5,exp=50,gold=15,healthpots=1,manapots=1)

# Creating tuple linked to the characterstats dataframe. This tuple will be used to assign the values 
# of the "normalbattlereturn" tuple to the actual character attributes
# Format of this tuple is [(row index),(column index),(abbreviated dataframe name)]
characterresults = [('user','hitpoints','charStats'),('user','exp','charStats'),('user','gold','charStats'),('Health Potion','numberHeld','currentItems'),('Mana Potion','numberHeld','currentItems')]
# Setting starting parameters
maxHitpoints = 25
maxMana = 25


### Creating dataframes for stats
## Character stats
characterNames = pd.Series(['user'])
characterStats = pd.DataFrame({'hitpoints' : pd.Series([25]),
                                   'mana' : pd.Series([25]),
                                   'strength' : pd.Series([5]),
                                   'agility' : pd.Series([5]),
                                   'intelligence' : pd.Series([5]),
                                   'maxHitpoints' : pd.Series([maxHitpoints]),
                                   'maxMana' : pd.Series([maxMana]),
                                   'exp' : pd.Series([0]),
                                   'gold' : pd.Series([0]),
                                   'expToLvl' : pd.Series([200])})
characterStats.index = characterNames

## Monster Stats
monsterNames = pd.Series(['zombie', 'wisp', 'hobgoblin', 'neonazi', 'stevejobs'])
monsterStats = pd.DataFrame({ 'hitpoints' : pd.Series([40, 20, 25, 30, 40]),
                                   'strength' : pd.Series([3, 1, 5, 4, 2]),
                                   'agility' : pd.Series([2, 4, 3, 2, 4]),
                                   'intelligence' : pd.Series([1, 5, 2, 1, 8]),
                                   'weaponeqp' : ['Zombie Hands', 'wispbeam', 'goblinclub', 'burningcross', 'ipadmini'],
                                   'gold' : pd.Series([20, 15, 80, 60, 500]),
                                   'exp' : pd.Series([50, 50, 100, 60, 100])})
monsterStats.index = monsterNames


## Weapon stats
weaponNames = pd.Series(["Jacob's Staff", "Talc Sword", "Orthoclase Spear", 
                             "Zombie Hands", "wispbeam", "goblinclub",
                             "burningcross", "ipadmini"])
weaponStats = pd.DataFrame({'weaponDamage' : pd.Series([5, 7, 25, 
                                                        2, 1, 5,
                                                        3, 2])})
weaponStats.index = weaponNames

## Items
itemNames = pd.Series(["Health Potion", "Mana Potion"])
itemStats = pd.DataFrame({'valueRest' : pd.Series([20,20]),
                              'attrRestName' : pd.Series(['hitpoints','mana']),
                              'maxAttrForChar': pd.Series([maxHitpoints,maxMana])})
itemStats.index = itemNames

# Currently eqipped items - make sure defaults are correct
currentItemNames = itemNames
currentItemsHeld = pd.DataFrame({'numberHeld' : pd.Series([2,2])})
currentItemsHeld.index = currentItemNames

### Defining general functions

def endgame():
    print("\nYou have died. Game over, nerd.")
    return

def damagecalc(wpnDmg, chrStr):
    critnumber = np.random.randint(0, high=100)
    if critnumber < 95:
        dmg = int(wpnDmg) + int(chrStr)*np.random.uniform(low=0.5, high=1.0)
        return int(dmg)
    elif critnumber >= 95:
        print("Gneiss hit!")
        dmg = int(wpnDmg) + int(chrStr)*np.random.uniform(low=1.1, high=1.4)
        return int(dmg)

# def successrun(): # Need to create place to return to after successful run
    

def normalbattle(enemy, characterStats):
    battleoptions = range(1,4)
    print('\n'+username+' has entered battle with '+enemy+'!\n')
    currentenemy = monsterStats.loc[enemy]
    damagetaken = 0
    manalost = 0
    healthPotionsLost = 0
    manaPotionsLost = 0
    battleaction = 'none'
    while battleaction not in str(battleoptions): # Default battleaction is 'none', so input one until it's in the battleoptions list
        print(currentenemy)
        print("\nYou have "+str((characterStats.at['user','hitpoints']) - damagetaken)+" health left.")
        print("You have "+str((characterStats.at['user','mana']) - manalost)+" mana left.\n")
        print("1) Attack")
        print("2) Use an item")
        print("3) Run")
        battleaction = input("What do you do? ")
        if battleaction == '1':
            while damagetaken < characterStats.at['user','hitpoints'] and battleaction == '1': # While you are alive
                dmgdealt = damagecalc(wpnDmg=weaponStats.at[str(equippedweapon),'weaponDamage'],chrStr=characterStats.at['user','strength'])
                print("You hit "+enemy+" for "+str(dmgdealt)+" damage.")
                currentenemy['hitpoints'] = int(currentenemy['hitpoints'] - dmgdealt)
                if currentenemy['hitpoints'] <= 0: # If they enemy is dead
                    hpafterbattle = int(characterStats.at['user','hitpoints'] - damagetaken)
                    print("You have defeated "+enemy+'!')
#                    return int(hpafterbattle) # This is assigned to the value of character's new health
                    # Creating named tuple with results of the battle
                    batresult = normalbattlereturn(hp=hpafterbattle,exp=int(currentenemy['exp']),
                                                   gold=int(currentenemy['gold']),healthpots=int(currentItemsHeld.loc['Health Potion','numberHeld'] - 
                                                           healthPotionsLost),manapots=int(currentItemsHeld.loc['Mana Potion','numberHeld'] - manaPotionsLost))
                    if characterStats.loc['user', 'exp'] >= characterStats.loc['user', 'expToLvl']:
                        levelup(characterStats)
                    return batresult
                elif currentenemy['hitpoints'] > 0: # If the enemy is alive
                    enemydmgdealt = damagecalc(wpnDmg=weaponStats.at[currentenemy['weaponeqp'],'weaponDamage'],chrStr=monsterStats.loc[enemy,'strength'])
                    print(enemy+' hits you for '+str(enemydmgdealt)+' damage.')
                    damagetaken = damagetaken + enemydmgdealt
                    if damagetaken > characterStats.at['user','hitpoints']: # If the character dies. RIP
                        endgame() #RIP function
                        break
                    battleaction = 'none' # Breaks the while statement so that another option may be selected
        elif battleaction == '2': # Writing this now to use only potions, may have to change items to individual functions in the future
            lowerrangeoption = currentItemsHeld[currentItemsHeld['numberHeld'] > 0].shape[0]+1 # Work around to range starting with 0 - prob better way to do this
            itemoptionlist = range(lowerrangeoption)[1:lowerrangeoption]
            itemoptionlist = ''.join(str(e) for e in itemoptionlist)
            print("Items currently held:\n")
            print("1: "+currentItemsHeld.index.values[0]+" - "+str(currentItemsHeld.loc['Health Potion','numberHeld'] - healthPotionsLost)+" left in inventory.")
            print("2: "+currentItemsHeld.index.values[1]+" - "+str(currentItemsHeld.loc['Mana Potion','numberHeld'] - manaPotionsLost)+" left in inventory.")
#            print(currentItemsHeld) # Need to fix this to make a numbered list instead of displaying dataframe
            itemaction = input("Which do you use? ") 
            while itemaction not in itemoptionlist:
                itemaction = input("Which do you use? ")
            if itemaction == '1': # For health potion
                itemused = currentItemsHeld.index.values[0:1][0] # Selects name by index of first row
                attrRestoredName = itemStats.loc[itemused,'attrRestName']
                attrRestoredValue = itemStats.loc[itemused,'valueRest']
                attrMaxCharValue = itemStats.loc[itemused,'maxAttrForChar']
                if (characterStats.at['user',attrRestoredName] + attrRestoredValue) > attrMaxCharValue:
                    if healthPotionsLost == currentItemsHeld.loc['Health Potion','numberHeld']:
                        print("\nYou are out of health potions!\n")
                        itemaction = 'none'
                        battleaction = 'none'
#                    global characterStats
#                    characterStats.at['user',attrRestoredName] = attrMaxCharValue
                    else:
                        damagetaken = 0
                        healthPotionsLost = healthPotionsLost + 1
                        itemaction = 'none'
                        battleaction = 'none'
                else:
                    if healthPotionsLost == currentItemsHeld.loc['Health Potion','numberHeld']:
                        print("\nYou are out of health potions!\n")
                        itemaction = 'none'
                        battleaction = 'none'
#                    global characterStats
#                    characterStats.at['user',attrRestoredName] = characterStats.at['user',attrRestoredName] + attrRestoredValue
                    else:
                        damagetaken = 0
                        healthPotionsLost = healthPotionsLost + 1
                        itemaction = 'none'
                        battleaction = 'none'
            elif itemaction == '2': # For mana potion
                itemused = currentItemsHeld.index.values[1:2][0] # Selects name by index of first row
                attrRestoredName = itemStats.loc[itemused,'attrRestName']
                attrRestoredValue = itemStats.loc[itemused,'valueRest']
                attrMaxCharValue = itemStats.loc[itemused,'maxAttrForChar']
                if (characterStats.at['user',attrRestoredName] + attrRestoredValue) > attrMaxCharValue:
                    if manaPotionsLost == currentItemsHeld.loc['Mana Potion','numberHeld']:
                        print("\nYou are out of mana potions!\n")
                        itemaction = 'none'
                        battleaction = 'none'
#                    global characterStats
#                    characterStats.at['user',attrRestoredName] = attrMaxCharValue
                    else:
                        manalost = manalost - attrRestoredValue
                        manaPotionsLost = manaPotionsLost + 1
                        itemaction = 'none'
                        battleaction = 'none'
                else:
                    if manaPotionsLost == currentItemsHeld.loc['Mana Potion','numberHeld']:
                        print("\nYou are out of mana potions!\n")
                        itemaction = 'none'
                        battleaction = 'none'
#                    global characterStats
#                    characterStats.at['user',attrRestoredName] = characterStats.at['user',attrRestoredName] + attrRestoredValue
                    else:
                        manalost = manalost - attrRestoredValue
                        manaPotionsLost = manaPotionsLost + 1
                        itemaction = 'none'
                        battleaction = 'none'
        
#        elif battleaction == 3:
#            runningchance = np.random.randint(0,100)
#            if runningchance > 80:


def dobattle(enemy, characterStats): # This updates the character stats at the end of the battle - calls the main battle function
    batresult = normalbattle(enemy=enemy, characterStats=characterStats)
    for result in characterresults:
        if result[2] == 'charStats' and result[1] == 'hitpoints':
            characterStats.set_value(result[0],result[1],int(batresult.hp))
        elif result[2] == 'charStats' and result[1] == 'exp':
            characterStats.set_value(result[0],result[1],int(batresult.exp))
        elif result[2] == 'charStats' and result[1] == 'gold':
            characterStats.set_value(result[0],result[1],int(batresult.gold))
        elif result[2] == 'currentItems' and result[0] == 'Health Potion':
            currentItemsHeld.set_value(result[0],result[1],int(batresult.healthpots))
        elif result[2] == 'currentItems' and result[0] == 'Mana Potion':
            currentItemsHeld.set_value(result[0],result[1],int(batresult.manapots))

def levelup(characterStats):
    print('\nLevel up. Get those gains, son\n')
    choice = input('add +2 to which stat?\n1) Strength\n2) Agility\n3) Intelligence\n')
    if choice == 1:
        characterStats.set_value('user', 'strength', (characterStats.loc['user', 'strength'] + 2))
    if choice == 2:
        characterStats.set_value('user', 'agility', (characterStats.loc['user', 'agility'] + 2))
    if choice == 3:
        characterStats.set_value('user', 'intelligence', (characterStats.loc['user', 'intelligence'] + 2))
    characterStats.set_value('user', 'expToLvl', (characterStats.loc['user', 'expToLvl'] * 1.2))

def town(currenttown):
    print("\nWelcome to "+currenttown+"!")
    townoption = range(1,5)
    townaction = 'none'
    while townaction not in str(townoption):
        print("1) Sleep at the inn")
        print("2) Barter with a merchant")
        print("3) Explore the surrounding area")
        print("4) Leave town and move on\n")
        townaction = input("Enter a choice: ")
        if townaction == '1':
            print("\n\"Come and take a lode off,\"\n")
            print("You draw a few cross sections before the lead of your indigo colored pencil breaks.")
            print("Disheartened, you head to bed.")
            characterStats.set_value('user', 'hitpoints', characterStats.loc['user','maxHitpoints'])
            characterStats.set_value('user', 'mana', characterStats.loc['user','maxMana'])
            return town(currenttown)
        elif townaction == '2':
            print("\"My prices will rock your socks off:\"\n")
            # trade() function needs to be made
        elif townaction == '3':
            print("You decide to head out of", currenttown, "to explore.")
            explore(currenttown)
            return town(currenttown)
        elif townaction == '4':
            print("You decide that it's time to move on.")
            # nexttown() this function needs to be made
            return
            # return travel() function needs to be made
        
        
def explore(currenttown):
    monsterIndex = np.random.randint(0,len(monsterNames))
    enemy = monsterNames[monsterIndex]
    dobattle(enemy, characterStats)
    
    

#%%
#def randomencounter(): # This is called if the explore option is seleted from a town. May change this to have character level or town as an input, so that monsters will change as a function of level or location
    





username = input('Hello. What is your name? ')
print('Gneiss to meet you, ', username+'.')
print("Let's get geological.")
print('-'*60)
print('###CHAPTER 1###\n\n')
print("You awake in your tent at 6:00, ready to start mapping the geological contacts of Marquette in order to understand the area's tectonic history.\n")
print("Moments pass before you hear leaves crunching from footsteps not 10 feet away from you.")
print("You came alone on this field work. You are slightly unsettled by the sound of footsteps.\n") 
print("What do you do?\n")
print("1) Open up the doors and look outside")
print("2) Stay inside for now. Maybe it will wander away")
optionlist = range(1,3)
ch1tentaction = input("Enter a choice: ")
while ch1tentaction not in str(optionlist):
    print("Please enter a valid choice.")
    ch1tentaction = input("Enter a choice: ")

if ch1tentaction == '1':
    print("You unzip your tent door and step outside to see an undead abomination.")
    enemy = 'zombie'
    print("\"My studies in Earth Science have perfectly prepared me for this situation,\" you say as you pick up your Jacob's Staff.")
    equippedweapon = "Jacob's Staff"
    dobattle(enemy, characterStats)
        
        
    
elif ch1tentaction == '2':
    print('You decide that you\'ll wait for it to go away. "It\'s probably just an animal,\" you think to yourself.')
    print("The footsteps stop. Suddenly you hear heavy moaning and breathing.")
    print("\"What in tarnation?\" you say, quickly sitting up.")
    print("An undead abomination rips through your tent. It looks at you and mutters \"Mmmmm.\" It proceeds to have a delicious breakfast.")
    endgame()

print("\"Holy schist,\" you murmer as you take a moment to collect yourself.")
print("\"I've played enough video games to know where this is headed.\"")
print("You proceed to pack your things and make your way to Marquette. Field work will have to wait.\n\n\n")

currenttown = "Marquette"
town(currenttown)

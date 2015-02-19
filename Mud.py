#Michael Quinn Parkinson - MUD Sworderer
#Early release of a MUD I made a couple of years ago.
# There are some know bugs that have to do with traveling
#and fighting hard monsters. 
import random
import time
import pickle
import os
import sys


## Initial constants
initial_human = 100
human = initial_human
human_dead = 0
initial_beast = 30
beast = initial_beast
beast_dead = 0
accuracy_beast = 0.5
accuracy_human = 0.4
attack_speed_human = 1.0
attack_speed_beast = 0.9
crit_multi_human = 2.0
crit_multi_beast = 2.0
block_chance = 0.1
walk_speed = 1.0
armor_human = 0.0
armor_beast = 0.0
experience = 0
area = 1
level = 1
kills = 0
gold = 0
gold_chance = 0.15
level_increase_human = level
level_increase_beast = kills
upgrade = 1
area_advance = 0
start = time.time()
x_pos = 0
y_pos = 0
monster_probablity = 0.20
next_level = 5
strength_human = 1
dexterity_human = 1
health_human = 1
skill_spike_shield = 0
skill_double_attack = 0
craft_chance = 0.25
craft_item = 0
restart_answer = "yes"
## function for the beast attack
def beast_attack_roll(skill_spike_shield,beast,character_name,monster_level,level,accuracy_beast,crit_multi_beast,human,human_dead,x_pos,y_pos,armor_beast):
    human_dead = 0
    beast_attack = random.random()
    weapon_beast = random.uniform(monster_level,2+random.uniform(1,((1+x_pos**2 + y_pos**2)**(1.0/2.0))+(monster_level))) + random.uniform(monster_level,2+random.uniform(1,((1+x_pos**2 + y_pos**2)**(1.0/2.0))+(monster_level)))*random.uniform(0,area)
    print ""
    print "The Beast Attacks!"
    print ""
    if beast_attack >= accuracy_beast:
        time.sleep(attack_speed_beast)
        block_roll = random.random()
        if block_chance >= block_roll:
            print "The attack was blocked!"
            print ""
            beast = beast - skill_spike_shield
            if skill_spike_shield > 0:
                print "Spike shield did",skill_spike_shield,"damage to the beast."
                print ""
        else:
            if (weapon_beast >= 2.0*(((1+x_pos**2 + y_pos**2)**(1.0/2.0))+(monster_level + 1))) and (beast_attack >= accuracy_beast):
                print "The beast made a critical hit!"
                print ""
                weapon_beast = crit_multi_beast*weapon_beast
            deflection_human = (weapon_beast*armor_beast/100.0)
            if deflection_human > 0.01:
                print character_name,"deflected","%.2f" %deflection_human, "damage."
                print ""
            print "The attack does","%.2f" % abs((weapon_beast) - deflection_human), "damage."
            print ""
            human = human -abs((weapon_beast) - (weapon_beast*armor_beast/100.0))
        if human <= 0:
            print character_name,"has died!"
            human_dead = 1
        else:
            print character_name,"has","%.2f" %human,"life left."
            print ""
    else:
        print "The attack misses."
        print ""
        time.sleep(attack_speed_beast)
    return (beast,human,human_dead)
## function for the human attack
def human_attack_roll(skill_double_attack,character_name,strength_human,level,accuracy_human,crit_multi_human,beast,beast_dead,armor_human):
    beast_dead = 0
    human_attack = random.random()
    weapon_human = (random.uniform(1+level,6 + level) + random.uniform(1+level,6 + level)*random.uniform(0,area) +random.uniform(1,6 + level)*strength_human/100.0)*upgrade
    print ""
    print character_name,"Attacks!"
    print ""
    if human_attack >= accuracy_human:
        if (weapon_human >= 2*(5+level)) and (human_attack >= accuracy_human):
            print character_name,"made a critical hit!"
            print ""
            weapon_human = crit_multi_human*weapon_human
            double_roll = random.random()
            if (double_roll < skill_double_attack):
                weapon_human = 2*crit_multi_human*weapon_human
                print "Double Attack!"
                print ""
        deflection_beast = (weapon_human*armor_human/100.0)
        if deflection_beast > 0.01:
            print "The beast deflected","%.2f" %deflection_beast, "damage."
            print ""
        print "The attack hits does","%.2f" % abs((weapon_human) - deflection_beast), "damage."
        print ""
        time.sleep(attack_speed_human)
        
        beast = beast - abs((weapon_human) - deflection_beast)
        if beast <= 0:
            beast_dead = 1
        else:
            print "The beast has","%.2f" %beast,"life left."
            print ""
    else:
        print "The attack misses."
        print ""
        time.sleep(attack_speed_human)
    return (beast,beast_dead)
## function for obtaining experience from a kill
def get_experience(monster_level,character_name,kills,experience,beast,initial_beast,crit_multi_beast,accuracy_beast,level_increase_beast,x_pos,y_pos,armor_beast,level):
    kills = kills + 1
    xp_increase = level + random.random()*((x_pos**2 + y_pos**2)**(1.0/2.0))*level
    print "The beast gives","%.2f" %xp_increase,"experience."
    print ""
    experience = experience + xp_increase
    print character_name,"has","%.2f" %experience,"experience."
    print ""
    beast = 10.1 + monster_level*10.1 
    intial_beast = beast
    accuracy_beast = accuracy_beast - 0.003
    crit_multi_beast = crit_multi_beast + 0.003
    armor_beast = armor_beast + 0.03
    return (experience,beast,initial_beast,accuracy_beast,crit_multi_beast,kills,armor_beast)
##displaces a map of the local area with respect to a town
def show_map(x_pos,y_pos):
    if (x_pos ==0) and (y_pos == 0):
        length = 2.0*((x_pos**2 + y_pos**2)**(1.0/2.0)) + 5
        local_map_town = [[0 for i in range(int(round(length)))] for j in range(int(round(length)))]
        local_map_town[int((length-1.0)/2.0)][int((length-1.0)/2.0)] = 2
        print "The local map. (1 you || 2 is a town)"
        print ""
        for row in local_map_town:
            print row
        print ""
    else:
        length = 2.0*((x_pos**2 + y_pos**2)**(1.0/2.0)) + 5
        X_pos = (x_pos + int((length-1.0)/2.0))
        Y_pos = (y_pos + int((length-1.0)/2.0))
        local_map_town = [[0 for i in range(int(round(length)))] for j in range(int(round(length)))]
        local_map_town[int((length-1.0)/2.0)][int((length-1.0)/2.0)] = 2
        local_map_town[Y_pos][X_pos] = 1
        print "The local map. (1 is the human || 2 is a town)"
        print ""
        for row in local_map_town:
            print row
        print ""
## function for leveling up the human. It increases base stats.
def level_up(character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,gold,kills,experience,level,human,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human,level_increase_human):
    while (experience > (next_level)):
        next_level = 2.1*experience
        level = level + 1
        print ""
        print "~~~/**\/LEVELUP\/**\~~~"
        print character_name," level is ", level
        print ""
        print "You are given one stat point."
        print ""
        stat_use = 1
        while(stat_use == 1):
            stat_answer = raw_input("Which stat to increase? (strength, dexterity, health)")
            print ""
            if (stat_answer == "strength") or (stat_answer == "str") or (stat_answer == "s"):
                strength_human = strength_human + 1.5
                stat_use = 0
            if (stat_answer == "dexterity") or (stat_answer == "dex") or (stat_answer == "d"):
                dexterity_human = dexterity_human + 1.5
                stat_use = 0
            if (stat_answer == "health") or (stat_answer == "hp") or (stat_answer == "h"):
                health_human = health_human + 2.5
                stat_use = 0
        human = initial_human + 1.25*health_human
        initial_human = human
        accuracy_human = accuracy_human - 0.005*dexterity_human
        attack_speed_human = attack_speed_human - 0.009*dexterity_human
        gold_chance = gold_chance + 0.05
        block_chance = block_chance + 0.01*strength_human
        crit_multi_human = crit_multi_human + 0.005
        walk_speed = walk_speed - 0.003*dexterity_human
        armor_human = armor_human + 0.03*strength_human
        save_character(character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human)
    return strength_human,dexterity_human,health_human,next_level,gold,kills,experience,level,human,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human
## function for saving the character data
def save_character(character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human):
    print "Saving Character Data."
    print ""
    path = sys.path[0]
    os.chdir(path)
    with open(character_name,"wb") as save_file:
        pickle.dump((craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human),save_file)
    save_file.close()
    print "Complete!"
    print ""
    print ""
## function for loading the data
def load_character(loading):
    loading = 1    
    while(loading ==1):
        character_name = raw_input("What is the human's name? ")
        print ""
        try:
            with open(character_name,"rb") as save_file:
                craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human = pickle.load(save_file)
        except IOError:
            print "Character name not found in data base!"
            print ""
            loading = 1
        else:
            with open(character_name,"rb") as save_file:
                craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human = pickle.load(save_file)
            save_file.close()
            loading = 0
            print "Character Found!"
            print ""
            print ""
            print "Loading old character."
            print ""
        
    return loading,character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human
## function for obtaining loot for a recent kill
def get_loot(craft_chance,craft_item,character_name,gold_chance,gold):
    roll = random.random()
    print character_name,"is collecting loot."
    print ""
    time.sleep(1)
    if craft_chance >= roll:
        print ""
        print "The beast had a bit of metal in it..."
        print ""
        craft_item = craft_item + 1
    if gold_chance >= roll:
        print character_name,"collected gold!"
        print ""
        print ""
        gold = gold + 1
    else:
        print character_name,"found nothing else."
        print ""
        print ""
    return craft_item,gold
## function for late game advancement
def area_advancement(character_name,monster_level,area_advance,area,kills,level_increase_human,level_increase_beast):
    area_advance = area_advance + (50 + area**area) 
    if kills == area_advance:
        area = area + 1
        print character_name,"travels to area ",area,"."
        print ""
        time.sleep(2*walk_speed)
        level_increase_human = random.uniform(1,level)
        level_increase_beast = random.uniform(1,monster_level)
    return (area,level_increase_human,level_increase_beast)
## function for the initial start screen
def start_game(craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human):
    loading = 1
    while(loading == 1):
        print "Loading..."
        time.sleep(1)
        print ""
        print " $$$$$$\                                          $$\  "                                       
        print "$$  __$$\                                         $$ |  "                                      
        print "$$ /  \__|$$\  $$\  $$\  $$$$$$\   $$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\ " 
        print "\$$$$$$\  $$ | $$ | $$ |$$  __$$\ $$  __$$\ $$  __$$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ "
        print " \____$$\ $$ | $$ | $$ |$$ /  $$ |$$ |  \__|$$ /  $$ |$$$$$$$$ |$$ |  \__|$$$$$$$$ |$$ |  \__| "
        print "$$\   $$ |$$ | $$ | $$ |$$ |  $$ |$$ |      $$ |  $$ |$$   ____|$$ |      $$   ____|$$ | "     
        print "\$$$$$$  |\$$$$$\$$$$  |\$$$$$$  |$$ |      \$$$$$$$ |\$$$$$$$\ $$ |      \$$$$$$$\ $$ | "     
        print " \______/  \_____\____/  \______/ \__|       \_______| \_______|\__|       \_______|\__| "     


        print ""
        print "Alpha Version"
        print ""
        print ""
        save_answer = 1
        save_load = 0
        while(save_answer == 1):
            save_load = raw_input("New character or Load a game? ")
            print ""
            if (save_load == "load") or (save_load == "Load") or (save_load == "l"):
                print ""
                print "Current saved characters: "
                print ""
                print ""
                path = sys.path[0]
                os.chdir(path)
                i = 0
                for files in os.listdir("."):
                    if files.endswith(""):
                        if files == "game.py":
                            continue
                        else:
                            i = i + 1
                            
                            print ""
                            print i,files
                            print ""
                if i == 0:
                    print ""
                    print "There are no saved characters."
                    print ""
                    save_answer = 0
                    loading = 0
                    save_load = "new"
                else:
                    loading,character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human = load_character(loading)
                    save_answer = 0
                loading = 0
            if(save_load == "new") or (save_load == "New") or (save_load == "n"):
                print ""
                print "Starting new character."
                print ""
                character_name = raw_input("What is the human's name? ")
                for i in range(5):
                    print ""
                    time.sleep(0.1)
                print "A battered fighter named",character_name,"sits in a dark corner of a pub, drifting into a dream."
                print ""
                time.sleep(1)
                print "."
                print ""
                time.sleep(1)
                print ".."
                print ""
                time.sleep(2)
                print "..."
                print ""
                time.sleep(3)
                loading = 0
                save_answer = 0
            else:
                continue

            
    return character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human
## function for the decision of each turn. Current options (shop, travel, character, explore, leave)
def movement_human(save_leave,craft_item,upgrade,skill_double_attack,skill_spike_shield,level_increase_human,restart_answer,characters_name,health_human,strength_human,dexterity_human,next_level,area,kills,level,experience,gold,x_pos,y_pos,human):
    repeat = 0
    monster_roll = random.random()
    while(repeat == 0):
        if (x_pos == 0) and (y_pos == 0):
            print ""
            print character_name,"is in a town."
            print ""
        answer = raw_input("What is your next move? (shop, travel, character, explore, leave): ")
        print ""
        if(answer == "shop") or (answer == "s"):
            print character_name,"is traveling back to town."
            print ""
            time.sleep(((x_pos**2 + y_pos**2)**(1.0/2.0))*walk_speed)
            x_pos = 0
            y_pos = 0
            store_answer = raw_input("Where would like to shop at? (skills, health, pub, craft, upgrade, back): ")
            print ""
            if (store_answer == "skills") or (store_answer == "s"):
                print ""
                print character_name,"is traveling to the store."
                print ""
                time.sleep(((x_pos**2 + y_pos**2)**(1.0/2.0))*walk_speed)
                print ""
                print "The available spells are: "
                print ""
                print "Spiked Shield. Adds damage to blocked attacks. 5 Gold"
                print "Each level increases damage done."
                print ""
                print "Double Attack. Double attacks on critical hits. 5 Gold"
                print "Each level increases chance of occurance."
                print ""
                hp_answer = raw_input("Do you wish to buy Spiked Shield (ss) or Double Attack (da) or none? (ss  da  none)")
                if (hp_answer == "ss") or (hp_answer == "Spiked Shield") or (hp_answer == "spiked shield"):
                    if gold >= 5:
                        gold = gold - 5
                        print "Skill increased by ", 1
                        skill_spike_shield = skill_spike_shield + 1
                        repeat = 1
                    else:
                        print ""
                        print "Not enough gold!"
                        print ""
                        repeat = 1
                if (hp_answer == "da") or (hp_answer == "Double Attack") or (hp_answer == "double attack"):
                    if gold >= 5:
                        gold = gold - 5
                        print "Skill increased by ", 1
                        skill_double_attack = skill_double_attack + 0.1
                        repeat = 1
                    else:
                        print ""
                        print "Not enough gold!"
                        print ""
                        repeat = 1
                else:
                    print "Good Bye"
                    print ""
                    repeat = 1
            if (store_answer == "health") or (store_answer == "h"):
                print ""
                print character_name,"is traveling to the store."
                print ""
                time.sleep(((x_pos**2 + y_pos**2)**(1.0/2.0))*walk_speed)
                print ""
                print "A permanent upgrade to your health costs 10 gold."
                print ""
                hp_answer = raw_input("Do you wish to buy it? (yes or no)")
                if (hp_answer == "yes") or (hp_answer == "y"):
                    if gold >= 10:
                        gold = gold - 10
                        print "Health increased by", level_increase_human
                        human = human + level_increase_human*1.25
                        repeat = 1
                    else:
                        print ""
                        print "Not enough gold!"
                        print ""
                        repeat = 1
                else:
                    print "Good Bye"
                    print ""
            if (store_answer == "upgrade") or (store_answer == "u"):
                print character_name," is traveling to the store."
                print ""
                time.sleep(((x_pos**2 + y_pos**2)**(1.0/2.0))*walk_speed)
                print ""
                print "A permanent upgrade to your damage costs 100 gold."
                print ""
                da_answer = raw_input("Do you wish to buy it? (yes or no)")
                if (da_answer == "yes") or (da_answer == "y"):
                    if gold >= 100:
                        gold = gold - 100
                        print "Damage is increased by two."
                        upgrade = upgrade + 2
                        repeat = 1
                    else:
                        print ""
                        print "Not enough gold!"
                        print ""
                        repeat = 1
                else:
                    print "Good Bye"
                    print ""
            if (store_answer == "pub") or (store_answer == "p"):
                print ""
                print character_name,"crawls to town's pub to drink."
                print ""
                time.sleep(10 + ((x_pos**2 + y_pos**2)**(1.0/2.0))*walk_speed)
                human = initial_human
                area = 1
                repeat = 1
                print ""
                print "Burp!"
                print ""
                print character_name,"health has been restored."
                time.sleep(5)
            if (store_answer == "back") or (store_answer == "b"):
                repeat = 1
            if (store_answer == "craft") or (store_answer == "c"):
                print ""
                print "Craft a better sword for 100 metal bits."
                print ""
                if craft_item >= 100:
                    craft_item = craft_item - 100
                    print "Your sword has been upgraded."
                    print ""
                    upgrade = upgrade + 1
                else:
                    print ""
                    print "You do not have enough metal bits."
        while((answer == "travel") or (answer == "t")):
            monster_roll = random.random()
            travel_answer = raw_input("Where will you go? (north, east, south, west, stay): ")
            print ""
            if (travel_answer == "west") or (travel_answer == "east") or (travel_answer == "north") or (travel_answer == "south") or (travel_answer == "w") or (travel_answer == "a") or (travel_answer == "s") or (travel_answer == "d") :
                if (travel_answer == "west") or (travel_answer == "a"):
                    x_pos = x_pos - 1
                    travel_answer = "west"
                if (travel_answer == "east") or (travel_answer == "d"):
                    x_pos = x_pos + 1
                    travel_answer = "east"
                if (travel_answer == "north") or (travel_answer == "w"):
                    y_pos = y_pos - 1
                    travel_answer = "north"
                if (travel_answer == "south") or (travel_answer == "s"):
                    y_pos = y_pos + 1
                    travel_answer = "south"
                    print ""
                print character_name,"wanders",travel_answer, ", deeper into the forest."
                print ""
                time.sleep(walk_speed)
                if (monster_roll >= 0.25) or (x_pos == 0) and (y_pos == 0):
                    repeat = 1
                    answer = 0
                else:
                    print ""
                    print "There seems to be no beasts here."
                    print ""
                    ore_roll = random.random()
                    if ore_roll >= craft_chance:
                        print ""
                        print "There is some ore in this field to mine."
                        craft_item = craft_item + 1
                        print character_name,"has collected a metal bit."
                        print ""
                    else:
                        print "This is an empty field."
                        print ""
                        continue
                        monster_roll = 0
            if (travel_answer == "stay"):
                x_pos = x_pos
                y_pos = y_pos
                answer = 0
                repeat = 1
                monster_roll = 0
        if (answer == "character") or (answer == "c"):
            elapsed = (time.time() - start)
            print ""
            print "The human's name is",character_name
            print "%.2f" %human, "life."
            print "%.2f" %strength_human, "strength."
            print "%.2f" %dexterity_human, "dexterity."
            print "%.2f" %health_human, "health."
            print "Killed", kills, "beasts."
            print "Double Attack: ",skill_double_attack
            print "Spike Shield: ",skill_spike_shield
            print character_name,"is level" , level
            print "Current experience: ","%.2f" % experience
            difference = (next_level) - experience
            print "Experience to next level","%.2f" % difference
            print gold, "gold was collected."
            print craft_item, "metal bits collected."
            print ""
        if (answer == "explore") or (answer == "e"):
            show_map(x_pos,y_pos)
        if (answer == "leave"):
            save_leave = 1
            answer = 0
            repeat = 1
            restart_answer = "no"
            monster_roll = 0
    return (save_leave,upgrade,craft_item,skill_spike_shield,skill_double_attack,gold,restart_answer,x_pos,y_pos,monster_roll,human)
## function for the exit screen
def human_death(character_name,experience,level,area,kills,start):
    elapsed = (time.time() - start)
    print ""
    print "The highest area reached was ", area
    print "killed", kills, "beasts."
    print character_name,"was level", level
    print "with",experience, "experience."
    print gold, "gold was collected."
    print character_name,"wandered the forest for ",elapsed/60, "minutes."
    print ""
    time.sleep(1)
    print "."
    print ""
    time.sleep(1)
    print ".."
    print ""
    print character_name,"awakes in a dimmly lit pub."
###########################################################################################################################################################################
###########################################################################################################################################################################
##Actual running of programs
while(restart_answer == "yes"):
    character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human = start_game(craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human)
    while(human > 0):
        save_leave = 0
        save_leave,upgrade,craft_item,skill_spike_shield,skill_double_attack,gold,restart_answer,x_pos,y_pos,monster_roll,human = movement_human(save_leave,craft_item,upgrade,skill_double_attack,skill_spike_shield,level_increase_human,restart_answer,character_name,health_human,strength_human,dexterity_human,next_level,area,kills,level,experience,gold,x_pos,y_pos,human)
        if save_leave == 1:
            save_character(character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,human,gold,kills,experience,level,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human)
            human = -1
        else:
            if (x_pos == 0) and (y_pos == 0):
                print ""
                print character_name,"is arriving to a town."
                print ""
                continue
            if (monster_roll >= 0.25):
                monster_level = random.randint(level-1,level+1)
                epic_monster = random.random()
                if epic_monster > 0.985:
                    monster_level = monster_level + 4
                    gold = gold + 5
                    print ""
                    print "An epic level",monster_level,"monster appears in the forrest."
                    print ""
                else :
                    print ""
                    print "A level",monster_level,"beast appears in the forrest."
                    print ""
                time.sleep(0.2)
                print ""
                beast = 10.1 + monster_level*10.1
                while(beast > 0):
                    if human_dead == 1:
                        break
                    beast,human,human_dead = beast_attack_roll(skill_spike_shield,beast,character_name,monster_level,level,accuracy_beast,crit_multi_beast,human,human_dead,x_pos,y_pos,armor_beast)
                    if human_dead == 1:
                        break
                    beast, beast_dead = human_attack_roll(skill_double_attack,character_name,strength_human,level,accuracy_human,crit_multi_human,beast,beast_dead,armor_human)
                    if beast_dead == 1:
                        print ""
                        print "The beast has been killed!"
                        print ""
                        experience,beast,initial_beast,accuracy_beast,crit_multi_beast,kills,armor_beast = get_experience(monster_level,character_name,kills,experience,beast,initial_beast,crit_multi_beast,accuracy_beast,level_increase_beast,x_pos,y_pos,armor_beast,level)
                        strength_human,dexterity_human,health_human,next_level,gold,kills,experience,level,human,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human = level_up(character_name,craft_item,skill_double_attack,skill_spike_shield,strength_human,dexterity_human,health_human,next_level,gold,kills,experience,level,human,initial_human,accuracy_human,attack_speed_human,gold_chance,block_chance,crit_multi_human,walk_speed,armor_human,level_increase_human)
                        craft_item,gold = get_loot(craft_chance,craft_item,character_name,gold_chance,gold)
                        area,level_increase_human,level_increase_beast = area_advancement(character_name,monster_level,area_advance,area,kills,level_increase_human,level_increase_beast)
                        beast_dead = 0
                        break
                
            if human_dead == 1:
                    break
    human_death(character_name,experience,level,area,kills,start)
    if restart_answer == "yes":
        x_pos = 0
        y_pos = 0
        human_dead = 0
        restart_answer = raw_input("Want to play again? (yes or no)")

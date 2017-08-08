import mwclient
import re
import json

site = mwclient.Site('feheroes.gamepedia.com', path = '/')
page = site.Pages['Hero List']
list_of_names = []
names = [x for x in page.links()]


for x in names:
        temp = re.search(r"'b'(.+?)''|\"", str(x))
        list_of_names.append(temp.group(1))
    
#clearing 'None' entries from way I got the list of names
temp = [x for x in list_of_names if (x != None) 
    and (x != 'None') and (x != 'Special Maps')]
list_of_names = temp
"""
page.text(2) is weapons
page.text(3) is assists
page.text(4) is special
page.text(5) are passives (all of them, so take care)
"""

output_dictionary = {}

#edit here to add more things to the data extracted from wiki

for x in list_of_names:
    #getting the list of weapon names

    weapon_list = []
    temp = re.findall(r"weapon\d=(.+)", site.Pages[x].text(2))
    for y in temp:
        weapon_list.append(y)
    output_dictionary[x] = {'Weapons' : weapon_list}
    
    #getting a, b, c passives
   
    
    a_passive_list = []
    temp = re.findall(r"passiveA\d=([\w \+]+)", site.Pages[x].text(5))
    for y in temp:
        a_passive_list.append(y)
    output_dictionary[x]['A_Passives'] = a_passive_list
    
    b_passive_list = []
    temp = re.findall(r"passiveB\d=([\w \+]+)", site.Pages[x].text(5))
    for y in temp:
        b_passive_list.append(y)
    output_dictionary[x]['B_Passives'] = b_passive_list
    
    c_passive_list = []
    temp = re.findall(r"passiveC\d=([\w \+]+)", site.Pages[x].text(5))
    for y in temp:
        c_passive_list.append(y)
    output_dictionary[x]['C_Passives'] = c_passive_list
    
    #getting specials
    
    special_list = []
    temp = re.findall(r"special\d=([\w ]+)", site.Pages[x].text(4))
    for y in temp:
        special_list.append(y)
    output_dictionary[x]['Specials'] = special_list
    
    #getting color and weapon type (neutral = colorless)
    
    color = ''
    weapon_type = ''
    temp = re.findall(r"class ?= ?(\w+) (\w+)", site.Pages[x].text(0))
    print(x)
    print(temp)
    if (temp):
        color = temp[0][0]
        weapon_type = temp[0][1]
    output_dictionary[x]['Color'] = color
    output_dictionary[x]['Weapon Type'] = weapon_type
    
    
    #getting movement type
    
    temp = re.findall(r"Attribute ?= ?(\w+)", site.Pages[x].text(0))
    movement_type = temp[0]
    output_dictionary[x]['Movement'] = movement_type
    
    #getting 5* base stats, only going to output level 40 stats for now
    
    hp = []
    atk = []
    spd = []
    defense = []
    res = []
    
    temp = re.findall(r"Icon Rarity 5.+?span>(.+?)</table>", site.Pages[x].text(
        0, expandtemplates=True))
    stats = re.findall(r"<td>(.+?)</td>", str(temp))
    level_1_stats = stats[0:5]
    level_40_stats = stats[5:10]
    
    hp = level_40_stats[0]
    atk = level_40_stats[1]
    spd = level_40_stats[2]
    defense = level_40_stats[3]
    res = level_40_stats[4]
    
    level_40_stats_dictionary = { 'Hp' : hp, 'Attack' : atk, 'Speed' : spd,
        'Defense' : defense, 'Resistance' : res}
        
    hp = level_1_stats[0]
    atk = level_1_stats[1]
    spd = level_1_stats[2]
    defense = level_1_stats[3]
    res = level_1_stats[4]   
    
    level_1_stats_dictionary = { 'Hp' : hp, 'Attack' : atk, 'Speed' : spd,
        'Defense' : defense, 'Resistance' : res}

    output_dictionary[x]['Level 40 Stats'] = level_40_stats_dictionary
    output_dictionary[x]['Level 1 Stats'] = level_1_stats_dictionary

print(json.dumps(output_dictionary, sort_keys=True, indent=4))

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
temp = [x for x in list_of_names if (x != None) and (x != 'None')]
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
    temp = re.findall(r"passiveA\d=([\w ]+)", site.Pages[x].text(5))
    for y in temp:
        a_passive_list.append(y)
    output_dictionary[x]['A_Passives'] = a_passive_list
    
    b_passive_list = []
    temp = re.findall(r"passiveB\d=([\w ]+)", site.Pages[x].text(5))
    for y in temp:
        b_passive_list.append(y)
    output_dictionary[x]['B_Passives'] = b_passive_list
    
    c_passive_list = []
    temp = re.findall(r"passiveC\d=([\w ]+)", site.Pages[x].text(5))
    for y in temp:
        c_passive_list.append(y)
    output_dictionary[x]['C_Passives'] = c_passive_list


print(json.dumps(output_dictionary, sort_keys=True, indent=4))

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
    temp = re.split(r"(weapon\d=)(.+)", str(site.Pages[x].text(2)))
    counter = 0
    for y in temp:
        counter += 1
        if (counter % 3 ) == 0:
            weapon_list.append(y)
      
    output_dictionary[x] = {'weapons' : weapon_list}

for x in output_dictionary:
        print("{")
        print("\"" + x + "\"")
        print(json.dumps(output_dictionary[x], sort_keys=True, indent=4))
        print("}")
    
#print('done')

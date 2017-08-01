import mwclient
import re

site = mwclient.Site('feheroes.gamepedia.com', path = '/')
page = site.Pages['Hero List']
list_of_names = []
list = page.links()
names = [x for x in page.links()]


for x in names:
        temp = re.search(r"'b'(.+?)''|\"", str(x))
        list_of_names.append(temp.group(1))
	
print (list_of_names)

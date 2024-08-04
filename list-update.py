import requests, json, time
from bs4 import BeautifulSoup

main_page = 'https://arknights.fandom.com'
table_page = '/wiki/Recruitment/Operators'

main_html = BeautifulSoup(requests.get(main_page+table_page).text, 'html.parser')
main_table = main_html.find('table', {'class': 'mrfz-wtable'})

link_dict = {}
tag_dict = {}

print("Fetching data from ", main_page+table_page)      #UXlog
for row in main_table.find_all('tr'):
    for column in row.find_all('td'):
        links = column.find_all('a', href=True)
        for link in links[1::2]:
            link_text = link.text.strip()
            link_url = main_page+link['href']
            link_dict[link_text] = link_url

taglist_page = '/wiki/Recruitment'
taglist = set() 
print("Getting list of all Recruitment tags from ",main_page+taglist_page)  #UXlog
taglist_html = BeautifulSoup(requests.get(main_page+taglist_page).text, 'html.parser')
taglist_table = taglist_html.find('table', {'class': 'mrfz-wtable'})
for row in taglist_table.find_all('tr'):
    taglist.update({tag.text.strip() for tag in row.find('td').find_all('span')})
print(f"Found {len(taglist)} Recruitment tags") #UXlog

print(f"\nGetting tags from {len(link_dict)} links")    #UXlog
for key in link_dict:
    op_html = BeautifulSoup(requests.get(link_dict[key]).text, 'html.parser')
    op_table = op_html.find('table', {'class': 'mrfz-btable'})
    #tags
    tags_row = op_table.find_all('tr')[2]
    tags = [tag.strip() for tag in tags_row.find_all('td')[1].text.split(',')]
    #position
    position_row = op_table.find_all('tr')[1]
    tags.extend([pos.strip() for pos in position_row.find_all('td')[1].text.split(',')])
    #stars, class, branch, faction
    role_row = op_table.find('tr').find('td')
    tags.extend([role.get('title').strip() for role in role_row.find_all('a') if role.get('title')])
    tag_dict[key] = tags
    print(f"Found {len(set(tags)&taglist)} tags for {key} ({len(tag_dict)}/{len(link_dict)})")   #UXlog

with open('tags.txt', 'w') as file:
    print(f"\nWriting tags to file: {file.name}")   #UXlog
    file.writelines([json.dumps({'recruitment tags': list(taglist), 'operator tags': tag_dict}), '\n\nUpdated: ', time.ctime()])

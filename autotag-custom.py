import requests, json, time
from bs4 import BeautifulSoup

main_page = 'https://arknights.fandom.com/wiki/'

with open('tags-custom.txt', 'r') as file:
    op_dict = json.loads(file.readline())

tag_dict = {}
for op in op_dict.keys():
    op_html = BeautifulSoup(requests.get(main_page+(cop:=op.capitalize()).replace(' ', '_')).text, 'html.parser')
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
    tag_dict[cop] = tags
    print(f"Found {len(set(tags))} tags for {cop} ({len(tag_dict)}/{len(op_dict)})")   #UXlog

with open('tags-custom.txt', 'w') as file:
    file.writelines([json.dumps(tag_dict), '\n\nUpdated: ', time.ctime()])

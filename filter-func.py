#nnoremap <c-x> :w<cr>:te py -i %<cr>
#tmp
from tabulate import tabulate

import json                     #file info to dictionary
import runpy                    #run update script when prompted
import sys                      #clean script termination
import re                       #regular expressions
import os                       #file path existence
from completefuzz import Finder as fzf
from completefuzz import Complete as fzc

#helper funcs

#def _help_msg(func='all'):
#    help_dialogue = {
#            'filter':"WiP",
#            'sort':"WiP",
#            'add':"WiP",}
#    return '\n\n'.join(help_dialogue.values()) #if func == 'all' else help_dialogue[help_category[0]]  

try:
    tagsfile = open('tags.txt', 'r')

except FileNotFoundError:
    while True:
        user_input = input("No tags file found. Create it now? [y/n] ")[0].lower()
        if user_input == 'n':
            sys.exit("No tags file found.")
        if user_input == 'y':
            runpy.run_path('list-update.py')
            tagsfile = open('tags.txt', 'r')
            break
        else:
            print("Invalid option: ", user_input)

#get tags from file
tags_dict = json.loads(tagsfile.readline())
operator_tags = tags_dict[fzf.findOne('op', tags_dict, type='consecutive')]
recruitment_tags = tags_dict[fzf.findOne('rec', tags_dict, type='consecutive')]
linked_tags = {fzf.findOne('top op', recruitment_tags): fzf.findOne('6star', (ot:=[item for sublist in operator_tags.values() for item in sublist])), fzf.findOne('senior', recruitment_tags):fzf.findOne('5star', ot)}


#UI functions
def filter(dict, tags):
    if not tags:
        return dict
    filtered = {key: val for key, val in dict.items() if tags[0] in val}
    return filter(filtered, tags[1:])

def sort(dict, tags):
    if not tags:
        return dict
    tagged = filter(dict, [tags[0]])
    tagless = {key: val for key, val in dict.items() if key not in tagged}
    return {**sort(tagged, tags[1:]), **tagless}

#def add(operators):
#    with open('tags-custom.txt', 'a+') as file:
#        if file.tell():
#            file.seek(0)
#            existing = json.loads(file.readline())
#            operators.extend(existing.keys())
#        file.truncate(0)
#        file.write(json.dumps(dict.fromkeys(operators, [])))
#        runpy.run_path('autotag-custom.py')

#def update():
#    runpy.run_path('list-update.py')
#    if os.path.exists('tags-custom.txt'):
#        runpy.run_path('autotag-custom.py')

#UI function handler
active_options = {}

def _parse_input(input_string):
    """
    syntax: function [+-]OPTIONS
            function [+-]OPTIONS [|/] function [+-]OPTIONS ...
        OPTIONS must be separated with a comma ','
        +OPTIONS adds OPTIONS to previous function call
        -OPTIONS removes OPTIONS from previous call
        OPTIONS (without prefix) overrides previous call
        prefix takes effect for all OPTIONS until next prefix or end of line
        if first OPTION has no prefix, all OPTIONS will be treated as such
        '|' (pipe) or '/' (slash) act as line separator
    """
    lines = re.split(r'[|/]', input_string)
    for line in lines:
        #separate function, options
        parts = line.split(' ', 1)
        function = parts[0].strip()
        options = [opt.strip() for opt in parts[1].split(',')]
        #parse function
        pfunc = fzc.func(function, globals())
        active_options.setdefault(pfunc, [])
        print("Action: ", pfunc.__name__)
        #parse options
        assert len(options), "no options given"
        if options[0].startswith(('+','-')):
            prefix=options[0][0]
            for opt in options:
                prefix = '+' if opt.startswith('+') else '-' if opt.startswith('-') else prefix
                so = fzf.findOne(opt.strip(prefix+' ,'), recruitment_tags)
                if prefix == '+' and so not in active_options[pfunc]:
                    active_options[pfunc].append(so)
                elif prefix == '-' and so in active_options[pfunc]:
                    active_options[pfunc].remove(so)
        else:
            active_options[pfunc] = [fzf.findOne(opt.strip('+-'), recruitment_tags) for opt in options]
        if not len(active_options[pfunc]):
            del active_options[pfunc]
        print("Values: ", ', '.join(active_options[pfunc]) if pfunc in active_options else "None\nAction removed")

def _execute(cmds):
    working_dict = operator_tags
    for cmd, args in cmds.items():
        if len(cmds[cmd]):
            working_dict = cmd(working_dict, args)
        else:
            del cmds[cmd]
    return working_dict

###########
#core loop#
###########
while True:
    try:
        wdict = _execute(active_options)
        table_data = []
        for k,v in wdict.items():
            table_data.append([k, ', '.join(v)])
        print(tabulate(table_data, tablefmt='grid'))
        print(active_options)
        cmd = input('>')
        if cmd == 'exit':
            break
        _parse_input(cmd)
    except:
        print("Invalid input: ", cmd)
sys.exit("Program terminated by user")

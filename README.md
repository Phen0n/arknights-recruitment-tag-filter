# arknights-recruitment-tag-filter
This is an extremely basic version of the full planned product. Stay tuned!
### Requirements
- Python 3.8+
PyPi packages:
-  BeautifulSoup
-  requests
-  tabulate

### Installation
Git:
```bash
git clone https://github.com/Phen0n/arknights-recruitment-tag-filter.git --depth 1
```
Direct:
- Go to *Code* -> *Download ZIP*
More options coming soon

Required Python packages
- run `pip install requests bs4 tabulate` in the terminal

### Usage
- Run *filter-func.py*
    - syntax: function [+-]OPTIONS
    - or:  function [+-]OPTIONS [|/] function [+-]OPTIONS ...
        - OPTIONS must be separated with a comma `,`
        - +OPTIONS adds OPTIONS to previous function call
        - -OPTIONS removes OPTIONS from previous call
        - OPTIONS (without prefix) overrides previous call
        - prefix takes effect for all OPTIONS until next prefix or end of line
        - if first OPTION has no prefix, all OPTIONS will be treated as such
        - `|` (pipe) or `/` (slash) act as line separator
    - functions: sort, filter
    - OPTIONS: any tag in the visible list

 ### To-do
 - Everything

## CompleteFuzz ##
## Version 3.10 ##
##  By  Phenon  ##

import re
import inspect

class Finder:
    @staticmethod
    def find(query, scope):
        """
        find(query(str), scope(iterable))
        return: {match:{'ratio':(float), 'consecutive':(float), 'combined':(float)}}
        """
        assert len(query), "Zero-length query"
        regex = re.compile( '.*'.join([re.escape(c) for c in query]), re.IGNORECASE)
        matches = [match for match in scope if regex.search(match)]
        if not len(matches):
            raise ValueError(f"No suitable matches found for query '{query}'")
        match_dict = {}
        #assign confidence values
        for match in matches:
            ratio = round((ql:=len(query))/len(match), 2)    #query length compared to match
            consecutive = 0
            for i in range(ql):                             #consecutive matched characters
                for j in range(i, ql):
                    if re.search(query[i:j+1], match, re.IGNORECASE):
                        consecutive = j+1-i if j+1-i > consecutive else consecutive
                    else:
                        break
            match_dict[match] = {'ratio': ratio, 'consecutive': (c:=round(consecutive/ql, 2)), 'combined': ratio*c}
        return match_dict
    
    @staticmethod
    def findOne(query, scope, type='ratio'): #types: ratio, consecutive, combined
        """
        return: match(str)
        """
        fzf_result = Finder().find(query, scope)
        max_type = lambda t: max(fzf_result, key=lambda k: fzf_result[k][t])
        return max_type(type)
#-----------------------------------------------------------------------------------------------------------------#
class Complete:
    @staticmethod
    def var(query, scope, type):
        """
        returns variable most closely matching the query
        scope: locals() or globals()
        """
        variable = Finder().findOne(query, [v for v in scope if type(v) is type(type)])
        return scope.get(variable)

    @staticmethod
    def func(query, scope):
        """
        return function most closely matching the query
        scope: locals() or globals()
        """
        function = Finder().findOne(query, [f for f in scope if inspect.isfunction(scope.get(f))])
        return scope.get(function)

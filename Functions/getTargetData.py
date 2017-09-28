__author__ = 'Jo'

import re


#Pass in: pattern surrounding text to find target data e.g. (links, link names, number of results, etc)
#Returns: an array of all instances of recognized pattern (Our Links in most cases)

def get_target_data(pattern, filez):
	patternz = re.compile(pattern)
	links = re.findall(patternz,filez)
	return links


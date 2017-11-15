__author__ = 'Jo'

import re


#Pass in: pattern surrounding text to find target data e.g. (links, link names, number of results, etc)
#Returns: an array of all instances of recognized pattern (Our Links in most cases)

def get_target_data(pattern, filez):
	regex = re.compile(pattern, re.S)
	#re.DOTALL
	links = regex.findall(filez)
	return links


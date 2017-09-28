__author__ = 'Jo'


from getWebpage import get_webpage


#Pass in: an index to store site data, and a list of links to get data from
#Returns: an index where index[i][0]=link, [i][1]=htmltext
    #This might not need an index Passed in...

def fill_index(indexz,full_linkz):
	i = 0
	indexz = []
	temp = []

	while i < len(full_linkz):
		temp = []
		temp.append(full_linkz[i])
		temp.append(get_webpage(full_linkz[i]))
		indexz.append(temp)
		i+=1
	return indexz
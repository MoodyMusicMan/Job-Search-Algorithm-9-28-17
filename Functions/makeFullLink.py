__author__ = 'Jo'

#Pass in: link list and root to append list to
#Returns: Index full of visit-able sites
    #This is necessary as when links to job postings are collected from Indeed.com,
    #they do not have the full address (they are missing 'the www.indeed.com/').

def make_full_link(linkz,rootz):
	i = 0
	url_destination=[]
	while i < len(linkz):
		url_destination.append(rootz + linkz[i])
		i+=1
	return url_destination
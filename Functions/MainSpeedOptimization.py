__author__ = 'Jo'

import time
from datetime import datetime
from fillIndex import fill_index
from getTitle import get_title
from getWebpage import get_webpage
from jobRater import job_rater

from Functions.getTargetData import get_target_data
from makeFullLink import make_full_link
from sortIndex import sort_index

#Note, you will need to rename the destination file



#Define initial conditions---------------------------------------------------------------------------------------------
#Create first web address to visit,
    # similar to the form
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Boston%2C+MA"
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Los+Angeles%2C+CA"
url_part1 = "http://www.indeed.com/jobs?q="     #The root of initial indeed.com searches
url_part2 = "Robotics+Engineering"              #Part where target job area is defined, with + inbetween multiple words
url_part3 = "&l=Boston%2C+MA"              #City with +'s inbetween, state with %2C+ before 2 letter abreviation
url_base = url_part1 + url_part2 + url_part3    #first web address


#Create text file to store results in------------------------------------------------------------------------------
currenTime = time.strftime("_%d.%m.%Y_%H.%M.%S")
write_text_page_name = "C:\Users\Jo\Documents/004_WebDev\UDAC_Portfolio/fullstack/vagrant\JobOffline/Results/" + url_part2 + url_part3 + currenTime + ".txt"
write_text_page = open(write_text_page_name,"w")


#Define patterns to search for-------------------------------------------------------------------------------------
link_style = '\nhref="(.+?)"'     #Pattern of our links to aggregate on indeed.com
name_style = '<title[^.]*>(.+?)</title>'        #Pattern of the name of a given job (Not Very Accurate)
search_count_style = '<div id="searchCount">Jobs[^.]*of (.+?)</div>'    #Pattern of "Total number of jobs" result


#Define KeyWords List-----------------------------------------------------------------------------------------------
keyword_list_master = []        #[[supers],[list]]
keyword_list = []               #[[value1, word1, word2, word3...][value2, word1, word2, word3]]
keyword_list_supers = []        #[[[threshold, points worth],[word1, word2, word3]], [], []...]
                                    #Note, any combination of  words from each super group will count towards threshold\
keyword_list = [

	[1,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware','prototy'],
	[10, 'control', 'electrical engineer', 'matlab', 'servo'],
	[30, 'plc', 'microcontroller'],
	[100, 'lab view', 'labview']
]

keyword_list_supers = [
	[[2,1000], ['Jr','Junior','entry level','new grad']],     #i.e. 1x 'entry level' + 1x 'new grad', or 2x 'entry level', etc
	[[2,-200],'senior','Sr. '],
	[[2,-1000], ['ph.d', 'phd', 'master\'s degree','masters degree', 'ms. degree', 'ms degree',' ms ']],
    [[1,-1000], ['7 years','7+ years','6 years','6+ years', '5 years','5+ years','9 years','9+ years']]
]
keyword_list_master.append(keyword_list_supers)
keyword_list_master.append(keyword_list)

startTime = datetime.now()
#Make our first Web request, and get on first page
urlfile = get_webpage(url_base)     #Make the first client request
search_count = get_target_data(search_count_style, urlfile)     #Grab the total number of job results
num_of_search_count = int(search_count[0])                      #Make search count into an int
print num_of_search_count



#-------------------------------------------------------------------------------#
#-----------------------------MAIN WHILE LOOP-----------------------------------#
#-------------------------------------------------------------------------------#


index = []                      #Our initial index to store everything in
urlTail = 0                     #keeps track of how many links we have aggregate
root = "http://indeed.com"      #Root to append link endings to later
url_start = url_base            #We will be modifying url_start later
linkList = []

while urlTail <= num_of_search_count:
    temp_index = []

    urlfile = get_webpage(url_start)                #Grab HTML from page
    links = get_target_data(link_style, urlfile)    #Grab Links from HTML
    for link in links:                              #Append links to linkList
        linkList.append(link)

    print url_start                                 #print out to know it's working
    urlTail +=10                                    #increment (goes to next page)
    url_start = url_base+'&start=' + str(urlTail)   #make next page url


full_links = make_full_link(linkList,root)          #Generate Full links from link list
index = fill_index(index, full_links)               #LARGEST STEP : Grabs HTML from all links, fills index with HTML

index = get_title(name_style, index)                #Searches for title in HTML
index = job_rater(index, keyword_list_master)       #Rates HTML based on Keywords
index = sort_index(index)                           #Sorts Index based on Score


print index[1][3]                       #Write second best score to screen

for a in index:                         #Write Index to TextFile
    write_text_page.write(str(a[3]) + ','+ str(a[4]) + ' : ' + a[2] + ' : ' + a[0])	##a[3] is type int, so needs to be forced str())
    write_text_page.write('\n')



totalTime = datetime.now() - startTime
print "Total Time Was : ", totalTime

#05:42:37100
#19:15:701
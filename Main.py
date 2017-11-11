'''
M0J01 - John Moody 

Last Revised 9/28/17
Python 2.7 tested only

The purpose of this program is to sort and rank job search results based on a persons weighted skills list

It outputs a Text File that contains 3 rows:
Total Points / num words | Total Points | Link to job 

Make sure you change the:
    Initial Conditions
    Directory to save output file
    Key Words List
    Key Words List Supers
        
The program should output print statements to the command line every time it starts a new page.
The program will also output any websites it could not read to the command line (These jobs will not be ranked)
^^ This is mostly due to inexperience with web protocals (i.e. AJAX... Curse you apple jobs!)

Thanks!
'''

__author__ = 'Jo'

import time
from datetime import datetime

from Functions.fillIndex import fill_index
from Functions.getTitle import get_title
from Functions.getWebpage import get_webpage
from Functions.jobRater import job_rater
from Functions.sortIndex import sort_index
from Functions.getTargetData import get_target_data
from Functions.makeFullLink import make_full_link

#DEFINE INITIAL CONDITIONS ---------------------------------------------------------------------------------------------
    #Create first web address to visit similar to the form;
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Boston%2C+MA"
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Los+Angeles%2C+CA"
    # ??? You can get this by typing a location/title of a job into indeed.com, and then porting it here

a = "http://www.indeed.com/jobs?q=Embedded+Systems&l=Miami%2C+FL"

# Search for a job in Indeed.com to make sure the initial formatting is right
#url_part1 = "http://www.indeed.com/jobs?q="     # - Leave Me - The root of initial indeed.com searches
#url_part2 = "Embedded+Systems"              # - Change Me - Part where target job area is defined, with + inbetween multiple words
#url_part3 = "&l=Miami%2C+FL"                   # - Change Me - City with +'s inbetween, state with %2C+ before 2 letter abreviation
#url_base = url_part1 + url_part2 + url_part3    #first web address

# LA
url_base = 'http://www.indeed.com/jobs?q=Microcontroller&l=Los+Angeles%2C+CA'

# CA
# Searched
#url_base = 'http://www.indeed.com/jobs?q=Embedded+Systems&l=CA'
url_part2 = 'Microcontroller'
url_part3 = 'LA'



print url_base

    #DEFINE DIRECTORY to store results in------------------------------------------------------------------------------
currenTime = time.strftime("_%d.%m.%Y_%H.%M.%S")
write_text_page_name = "C:/Users/M0J0/Documents/FOJ_2017/Python/Job-Results/" + url_part2 + url_part3 + currenTime + ".txt"
write_text_page = open(write_text_page_name,"w")

write_full_text_page_name = "C:/Users/M0J0/Documents/FOJ_2017/Python/Job-Results/" + "Full-Text" + currenTime + ".txt"
write_full_text_page = open(write_full_text_page_name,"w")

    #Define patterns to search for-------------------------------------------------------------------------------------
    # DO NOT CHANGE!!!
link_style = 'turnstileLink" href="(.+?)"'     #Pattern of our links to aggregate on indeed.com
name_style = '<title[^.]*>(.+?)</title>'        #Pattern of the name of a given job (Not Very Accurate)
#search_count_style = '<div id="searchCount">Jobs[^.]*of (.+?)</div>'    #Pattern of "Total number of jobs" result=
search_count_style = '[^.]*of (.+?)</div>'    #Pattern of "Total number of jobs" result=

    #Define KeyWords List Declaration-----------------------------------------------------------------------------------------------
    ## DO NOT CHANGE
keyword_list_master = []        #[[supers],[regulars]]
keyword_list = []               #[[value1, word1, word2, word3...][value2, word1, word2, word3]]
keyword_list_supers = []        #[[[ Appearence Threshold, points worth],[word1, word2, word3]], [[],[]], [[],[]]...] # Appears Threshold == if word is seen this many times or more

    #DEFINE KEY WORDS --------------------------------------------------------------------------------------------------
    # ----- MODIFY THESE VALUES TO FIT YOUR DESIRED JOB ------
keyword_list = [
                                        # Any of these words present in a job listing will add the first element worth of points to a job result
                                        # The code converts all letters to case letters
                                        # Use root words where possible i.e. "prototy" catches all conjugations of Prototyping
                                        # The formating sucks for single letter words. i.e "C" will be found inside ant word with a c, unless you treat it specialy. This is a known bug
	[10,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware', 'plc'],
	[10, 'control', 'electrical engineer', 'embedded sys', 'matlab', 'keras', 'Tensorflow', 'scikit learn', 'sklearn', 'canopen'],
	[30, 'microcontroller', 'servo', 'mcu', 'prototy', 'eagle'],
	[100, 'opencv', 'open cv', 'systems engineer']
]

keyword_list_supers = [                 #2 or more appearances for the words from the first list will award a 1 time bonus 1000 points
                                        #Note, any combination of  words from each super group will count towards threshold\
	[[2,2000], ['jr','junior','entry level','new grad']],     #i.e. 1x 'entry level' + 1x 'new grad', or 2x 'entry level', etc
    [[2,-2000], ['mechanical engineer']],
	[[3,-2000], ['senior','Sr. ']],          #I am not experienced enough to apply for Sr. level positions.
    [[2, -2000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms', 'masters' ]],
    [[3, -1000], ['nurse', 'technician']],  # NO NURSING POSITIONS PLEASE!
    #[[2, -1000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms ']], #Comment a line our if you don't want to use it anymore
    [[1,-1000], ['5 years','5+ years', '6 years','6+ years', '7 years','7+ years', '8 years', '8+ years', '9 years','9+ years', '10 years', '10+ years']]

]
keyword_list_master.append(keyword_list_supers)
keyword_list_master.append(keyword_list)

startTime = datetime.now()

#Make our first Web request, and get on first page
urlfile = get_webpage(url_base)     #Make the first client request
search_count = get_target_data(search_count_style, urlfile)     #Grab the total number of job results

#print urlfile
#print search_count

num_of_search_count = int(search_count[0].replace(',',''))                      #Make search count into an int
print ("There are :", num_of_search_count, " Results for :", url_part2, " jobs in the :", url_part3[2:], " area.") #url_part2 is the position title, url_part3 is the geographic area


#6:29:001100

#-------------------------------------------------------------------------------#
#-----------------------------MAIN WHILE LOOP-----------------------------------#
#-------------------------------------------------------------------------------#


index = []                      #Our initial index to store everything in
urlTail = 0                     #keeps track of how many links we have aggregate
root = "http://indeed.com"      #Root to append link endings to later
url_start = url_base            #We will be modifying url_start later

while urlTail <= num_of_search_count:
#while urlTail <= 5:
    temp_index = []

    urlfile = get_webpage(url_start)
    links = get_target_data(link_style, urlfile)
    #for a in links:
    #    print(a)
    full_links = make_full_link(links,root)
    temp_index = fill_index(temp_index, full_links)
    temp_index = get_title(name_style,temp_index)
    temp_index = job_rater(temp_index, keyword_list_master)

    #print(urlfile)
    for a in temp_index:
        print(a)
        index.append(a)

    print url_start
    urlTail +=10
    url_start = url_base+'&start=' + str(urlTail)


#
SearchTime = datetime.now() - startTime
print ("Web Search Time Was : ", SearchTime)
index = fill_index(index, full_links)
index = get_title(name_style, index)
index = job_rater(index, keyword_list_master)
#

index = sort_index(index)

#print index[1][3]

for a in index:
    write_text_page.write(str(a[3]) + ',' + str(a[4]) + ' : ' + a[0])  ##a[3] is type int, so needs to be forced str())
    write_text_page.write('\n')
    for item in a:
        write_full_text_page.write(str(item) + ' TOPANGO ')
    write_full_text_page.write(' TOPANGA ')

SortTime = datetime.now() - SearchTime
print "Total Time Was : ", SortTime
totalTime = datetime.now() - startTime
print "Total Time Was : ", totalTime

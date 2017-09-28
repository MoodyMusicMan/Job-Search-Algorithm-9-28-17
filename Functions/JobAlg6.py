__author__ = 'Jo'
import webbrowser	#Used for opening pages in a webbrowser
import urllib		#used for reading webpages
import re			#Used for parsing data
import mechanize  #Used for faking browser
import cookielib	#Used for populating fake browser with cookies

#It appears that the links on Indeed us either /rc or /cmp as links to jobs. Though they are always between 'href=" STUFF RIGHT HERE" target="_blank"'
#It appears that some of the links will not work unless the directing website is Indeed.com directly. I cannot access the sites from a cold URL (aka I cannot go to them directly... Future project is figure out how to go there from indeed first, though some of them do not seem to care, and just do not work...
#7/16/2015 1:34 AM, it apears some HTML tags with TITLE, have <title .....> name </title> in them. I must account for the ....
#7/16/2015 2:57 AM, it appears file.write() will only take in a string value, as such I must convert fromlist to string format first
#7/16/2015 6:02 AM, it may behoove my cause to convert all HTML inbound to lower case... however this would be difficult without downloading another function to facilitate, or some very very long checking functions... as of now I have a patched fix applied (Check for <title, and <TITLE>)... we will see if Patchwerk monster can get the job done.
#7/16/2015 7:22 AM, Keep up.
#7/16/2015 7:38 AM, There are some sites which I recieve an error page when I attempt to download the html data in to an object. So far Apple is one of the big ones.
#7/18/2015 8:00 AM, Added Mechanize Support, functional for the moment. I believe "AJAX" websites are causing some problems... Will need to investigate what AJAX is.

#----------Need to Fix--------------------
#	AJAX
#	DQ System
#	Repeated Listings
#	Scaled Ranking
#	"Perfect Job" - Rating
#	Better Keyword List
#-----------------------------------------





#-------------------------------------------------------------------------------#
#-----------------------------KEY PARAMETERS------------------------------------#
#-------------------------------------------------------------------------------#




#Define your base page here :: Make modular
url_base3 = "http://www.indeed.com/jobs?q=Robotics+Engineer&l=NYC%2C+NY"		#NewYork Base
url_base2 = "http://www.indeed.com/jobs?q=Robotics+Engineer&l=Boston%2C+MA"		#Boston Base
url_base1 = "http://www.indeed.com/jobs?q=Robotics+Engineer&l=California"		#California Base


#Select the type of search
base_selector = raw_input("1 : California \3 \n2 : Boston \3\n3 : NY \n\n")
field_selector = raw_input("\n\n1 : Robotics \3\n2 : Micro-Fabrication \3 \n3 : Mystery Select\n\n")

if base_selector == '3':
	url_base = url_base3
	write_text_page = open("NY_Robotics.txt","w")	#Define a PagetoWrite to here

elif base_selector == '2':
	url_base = url_base2
	write_text_page = open("BA_Robotics.txt","w")	#Define a PagetoWrite to here

else:
	url_base = url_base1
	write_text_page = open("CA_Robotics.txt","w")	#Define a PagetoWrite to here

print url_base


#Returned results will need to be appended to this to be accessable from outside indeed.com
root = "http://indeed.com"

#Define patterns to look for
link_style = 'href="(.+?)" target="_blank"'
name_style = '<title[^.]*>(.+?)</title>'
search_count_style = '<div id="searchCount">Jobs[^.]*of (.+?)</div>'


#Define your KeyWords here
#*****Add Regular Expression to allow for processing of correct 'C'****
keyword_list_master = []
keyword_list = []
keyword_list_supers = []

rank1 = [1,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware','prototy']
rank2 = [10, 'control', 'electrical engineer', 'matlab', 'servo']
rank3 = [30, 'plc', 'microcontroller']

keyword_list.append(rank1)
keyword_list.append(rank2)
keyword_list.append(rank3)

srank1 = [[1,10000], ['entry level','new grad']]
srank2 = [[1,1], ['test', 'stuff', 'here']]

keyword_list_supers.append(srank1)
keyword_list_supers.append(srank2)

keyword_list_master.append(keyword_list_supers)
keyword_list_master.append(keyword_list)


#-------------------------------------------------------------------------------#
#--------------------------------FUNCTIONS--------------------------------------#
#-------------------------------------------------------------------------------#


#Pass in: a url,
#Returns: an object containing the text of that URL
def get_webpage(url):

	#Set up mechanize and put in cookie jar
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	#Sets our Browser to handle Refreshes
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	#sets our Browser to immitate a browser
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	#Sets some cool stuff about handles the mechanize browser can do.
	br.set_handle_equiv(True)
	#br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	#Opens the URL given
	try:
		r = br.open(url)
		htmltextz = r.read()
		#htmltextz = htmltextz.lower() not gonna do this here. Messes with the tag searching.
	except:
		print url
		htmltextz = '0'

	return htmltextz

#Pass in: pattern outside of links and a text/object/file containing data to search
#Returns: all instances of recognized pattern (Our Links in most cases)
def get_target_data(patern, filez):
	patternz = re.compile(patern)
	links = re.findall(patternz,filez)
	return links

#Pass in: A list of links of link to open in a web-browser, a root webpage to concatenate the links to
#Returns: Null, though it will open some web pages!
#Not used ATM
def go_to_sites(linkz,rootz):
	for link in linkz:
		link = rootz+link
		webbrowser.open(link);
	return

#Pass in: link list and root to append list to
#Returns: Index full of visit-able sites
def make_full_link(linkz,rootz):
	i = 0
	url_destination=[]
	while i < len(linkz):
		url_destination.append(rootz + linkz[i])
		i+=1
	return url_destination

#Pass in: an index to store site data, and links to get data from
#Returns: an index where index[i][0]=sitelink, [i][1]=htmlinfo
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


#-------------------------------------------------------------------------------------------------
#Pass in: an index with index[i][0]=sitelink, [i][1]=htmlinfo
#Returns: an index where index[i][2]=job_name			##Based on extracted info
def get_name(indexz):

	i = 0
	while i < len(indexz):
		title = get_target_data(name_style,indexz[i][1])
		if title:
			title = str(title)
			indexz[i].append(title)
		else:
			start = indexz[i][1].find("<title>")
			end = indexz[i][1].find("</title>",start)
			if start == -1:
				start = indexz[i][1].find("<TITLE>")
				end = indexz[i][1].find("</TITLE>",start)
				if start == -1:
					start = indexz[i][1].find("<h1>")
					end = indexz[i][1].find("</h1>",start)
					title = indexz[i][1][start+4:end]
				else:
					title = indexz[i][1][start + 7 : end]
			else:
				title = indexz[i][1][start + 7:end]

			title = title.split()
			title = ''.join(title)
			#title = "['" + title + "']"
			indexz[i].append(title)

		i+=1
	return indexz

#--------------------------------------------------------------------------------------------------------------

#Pass in: Keyword list , and an index where index[i][0]=sitelink, [i][1]=htmlinfo, [i][2]=job_name
#Returns: an index with index[i][3]=Rating Count      	## Rating Count based on Keyword matching
#Need to work on the DQ logic. It is becoming too harsh and returns 0 qualified results for first 30 entries on indeed.
""" def rating_count(indexz,keywordz,dQz):

	dQindex = []

	i = 0
	while i < len(indexz):

		dQ_count = 0
		dQ_limit = 0
		ranks = 0
		count = 0

		while ranks < len(keywordz):

			word = 1
			multiplier = keywordz[ranks][0]		#print multiplier, '<< This is the multiplier \n'
			while word < len(keywordz[ranks]):

				match = re.findall(keywordz[ranks][word],indexz[i][1])		#print len(match), ' :: ', multiplier
				count += int(len(match))*int(multiplier)
				word+=1

			ranks+=1

		for items in dQz:
			dQ_Count = 0
			dQ_limit = items[0]
			dQ_Penatly = items[1]
			for word in items[2]:
				#for word in words:
				#print word
				matched = re.findall(word, indexz[i][1])
				dQ_Count += len(matched)
			if dQ_Count >= dQ_limit:
				print "DQ'ed"
				count += -1*dQ_Penatly
				print items[2]
				tempster = indexz[i]
				dQindex.append(tempster)
				tempster = []
				print indexz[i][2], indexz[i][0]

		indexz[i].append(count)
		i+=1
	return indexz, dQindex
"""
def rating_count(indexz,keyword_master):

	super_key = keyword_master[0]
	keywordz = keyword_master[1]

	i = 0
	while i < len(indexz):

		#dQ_count = 0
		#dQ_limit = 0

		ranks = 0
		count = 0
		sups_count = 0


		while sups_count < len(super_key):



			combo_break = super_key[sups_count][0][0]
			limit_break = super_key[sups_count][0][1]
			total_entry_number = 0

			for entry in super_key[sups_count][1]:
				match = re.findall(entry,indexz[i][1].lower())
				total_entry_number += int(len(match))


			if total_entry_number > combo_break:
				count+= limit_break
	
			sups_count +=1


		#	Iterate through the Keywordz >> keywordz[[m1,w1,w2,w3...],[m2,w1,w2,w3...],[m3,w1,w2,w3...]...]
		while ranks < len(keywordz):

			word = 1				#Because 0 is where the multiplier is stored... Lists of lists... Ba hum bug!
			multiplier = keywordz[ranks][0]				#print multiplier, '<< This is the multiplier \n'
			while word < len(keywordz[ranks]):			#Loop through the words in each rank of keyword

				#	Count the number o keyword matches, multiply by multiplier
				match = re.findall(keywordz[ranks][word],indexz[i][1].lower())		#Indexz[i][1] corresponds to the i'th index entry, and lower case html text of that entry. #print len(match), ' :: ', multiplier
				count += int(len(match))*int(multiplier)

				word+=1
			ranks+=1

		count2 = float(count) / len(indexz[i][1])
		indexz[i].append(count2)
		i+=1


	return indexz

#---------------------------------------------------------------------------------------------------------
#Pass in: an Unsorted Index
#Returns: an Sorted Index
def sort_index(indy):

	tempy = []			#temporary list to store new sorted elements in
	loco_sto = []		#tracks the location of the already sorted elements

	c = 0				#keeps track of # of elements sorted
	i = 1				#keeps track of current elements sorted

	max = 0				#keeps track of local max values for run through
	loco = 0			#local location element position

	while c < len(indy):
		while i < len(indy):
			if i not in loco_sto:
				if indy[i][3] > max:
					max = indy[i][3]
					loco = i
			i+=1
		loco_sto.append(loco)

		if indy[loco] not in tempy:
			tempy.append(indy[loco])

		max = 0
		i = 0
		c+=1

	return tempy


#Define your DQ List here
"""

#Make everything Lower Case --Look in to multithreading --getting rid of <Styles and such can increase speed
#Intro to NLP
dQ_list = []
dQ1 = [3, 10000, ['Nurse', 'nurse', 'NURSE']]
dQ2 = [10, 100, ['Senior', 'SENIOR', 'senior']]
dQ3 = [10, 100, ['health','Health','HEALTH']]
dQ4 = [4, 1000, ['oncology','Oncology','ONCOLOGY', 'physician', 'Physician', 'PHYSICIAN']]
dQ5 = [1, 1000, ['5+', '6+', '7+', '8+', '9+', '10+', '5 years', '6 years', '7 years', '8 years', '9 years', '10 years']]
dQ6 = [1, 1000, ['assist in surgery']]
dQ7 = [1, 10000, ['Chuck E. Cheese']]	#NO.
dQ8 = [1, 250, ['4+']]
dQ_list.append(dQ1)
dQ_list.append(dQ2)
dQ_list.append(dQ3) #It is not even added...
dQ_list.append(dQ4)
dQ_list.append(dQ5)
dQ_list.append(dQ6)
dQ_list.append(dQ7)
"""


#Define your index here
index = []

#Misnomer, actually meant to be the string to add to the end of the URL, not where the search will stop.
url_end = 0
url_start = url_base

#Get the number of search results
urlfile = get_webpage(url_start)
search_count = get_target_data(search_count_style,urlfile)
num_of_search_count = int(search_count[0])
print num_of_search_count




#-------------------------------------------------------------------------------#
#-----------------------------MAIN WHILE LOOP-----------------------------------#
#-------------------------------------------------------------------------------#




while url_end <= num_of_search_count:
	temp_index = []


	urlfile = get_webpage(url_start)
	links = get_target_data(link_style,urlfile)
	full_links = make_full_link(links,root)
	temp_index = fill_index(temp_index, full_links)
	temp_index = get_name(temp_index)
	temp_index = rating_count(temp_index,keyword_list_master)

	for a in temp_index:
		index.append(a)
	print url_start

	url_end += 10
	url_start = url_base+'&start=' + str(url_end)


		# write_text_page.write(str(a[3]) + ' : ' + a[2] + ' : ' + a[0])		##a[3] is type int, so needs to be forced str()
		# write_text_page.write('\n')


index = sort_index(index)
print index[1][3]

for a in index:
	write_text_page.write(str(a[3]) + ' : ' + a[2] + ' : ' + a[0])		##a[3] is type int, so needs to be forced str()
	write_text_page.write('\n')
"""
for b in dQQ:
	write_dQ_page.write(str(b[3]) + ' : ' + b[2] + ' : ' + b[0])
	write_dQ_page.write('\n')
print len(dQQ)
"""





	# new=2

# url="http://google.com";

# webbrowser.open(url,new=new);


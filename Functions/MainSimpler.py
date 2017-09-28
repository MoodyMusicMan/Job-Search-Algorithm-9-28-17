__author__ = 'Jo'

import mechanize
import cookielib
import re

############################################################
#
#                   Method Block
#
############################################################

def linkConstructor(agent):
    #Takes: a user agent [str(Job Location), str(Job Title)]
    #Gives: Link to WebSeed
    linkBase = 'http://www.indeed.com/jobs?q='
    linkPosition = ''
    linkLocation = ''
    linkMid = '&l='
    linkFinal = ''

    field = agent[0].split()
    location = agent[1].replace(",","")
    location = location.split()

    i = 0
    while i < (len(field) - 1):
        linkPosition += field[i] + '+'
        i+=1
    linkPosition+= field[-1]

    i = 0
    while i < (len(location) - 1):
        linkLocation += location[i] + '+'
        i+=1
    linkLocation += location[-1]

    linkFinal += linkBase+linkPosition+linkMid+linkLocation

    print linkFinal
    return linkFinal
def getWebpage(url):
    #Takes: Web url
    #Gives: Raw Text of that page

    #Set up mechanize and put in cookie jar
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	#Sets our Browser to handle Refreshes
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	#sets our Browser to immitate a browser
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	#Sets some cool stuff abut what mechanize browser can handle.
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
def getTargetData(pattern, file):
    #Takes: a Pattern and Text to search
    #Gives: all matchings of that pattern (used often for finding link results on website)
    pat = re.compile(pattern)
    links = re.findall(pat,file)
    return links

def userAttributesIndex(User):
    #Takes: User attributes in the DB from, User.degree, User.minors, .classesTaken... etc
    #Gives: index [strengthLevel, value] for all items in user
    #Could Consider writing a function call for each of these individually, and making values global
    degreePoints = 30
    minorsPoints = 25
    classesTakenPoints = 10
    personalTraitsPoints = 20
    hobbiesPoints = 20
    userL = []
    index = []

    userL.append([degreePoints,str(User.degree).replace(', ',',').split(',')])
    userL.append([minorsPoints,str(User.minors).replace(', ',',').split(',')])
    userL.append([classesTakenPoints,str(User.classesTaken).replace(', ',',').split(',')])
    userL.append([personalTraitsPoints,str(User.personalTraits).replace(', ',',').split(',')])
    userL.append([hobbiesPoints, str(User.hobbies).replace(', ',',').split(',')])

    for item in userL:
        for i in item[1]:
            tempL = []
            tempL.append(item[0])
            tempL.append(i)
            index.append(tempL)

    return index
def userSkillIndex(skills):
    #Takes: List of Skill Class from DB
    #Gives: Index [strengthLevel, Value] for all user skills]
    #FIX: multiple line spacing after a skill... i.e. '    ' will register as a skill
    index = []
    for skill in skills:
        ski = skill.skills.replace(', ', ',').split(',')
        for s in ski:
            if s != '' and s != ' ' :
                tempL = []
                tempL.append(skill.strengthLevel)
                tempL.append(s)
                index.append(tempL)

    return index

def getJobs(agent):
    #Takes: agent [jobtitle, location] agent
    #Gives: masterIndex, full of search results from running agent [indeed.com/link, link2, link3...]
    #Relies on: linkConstructor(), getWebpage(), getTargetData()
    searchCountStyle = '<div id="searchCount">Jobs[^.]*of (.+?)</div>'  #Format of # of results for querry
    linkStyle = '\nhref="(.+?)"'        #This will change from time to time... Current format list results are in
    masterIndex = []                    # [indeed.com/link, link2, link3...]

    seedAddress = linkConstructor(agent)
    firstText = getWebpage(seedAddress)
    numOfHits = int(getTargetData(searchCountStyle, firstText)[0].replace(',',''))
    returnedLinks = (getTargetData(linkStyle, str(firstText)))
    print numOfHits
    for link in returnedLinks:
        masterIndex.append('http://indeed.com'+link)


    #Scroll through all of the pages, grab all of the links
    i=10
    while i < numOfHits:
    #while i < 10:  #Used for rapid testing
        webAddress = seedAddress + '&start=' + str(i)
        print webAddress
        htmlText = getWebpage(webAddress)
        returnedLinks = getTargetData(linkStyle, str(htmlText))
        for link in returnedLinks:
            masterIndex.append('http://indeed.com'+link)
        i+=10

    return masterIndex  #full of links!
def rateJobs(skillIndex,jobIndex):
    #Takes: skillIndex [[power level,description],...], jobIndex [jobURL,...]
    #Gives: Index [[rating,jobURL],...]
    #Fix problems with the words C, HTML, and other commonly used non human significant characters.
    localIndex = []
    for job in jobIndex:
        count = 0
        text = str(getWebpage(str(job))).lower()
        for skill in skillIndex:
            strength = skill[0]
            word = str(skill[1]).lower()
            count+= int(strength)*bool(re.findall(re.escape(str(word)), text))         #.escape is used for when expressions like 'html' come up in re.
        tempI = []
        tempI.append(count)
        tempI.append(job)
        localIndex.append(tempI)

    return localIndex
def rankJobs(jobIndex):
    #Takes: rated jobIndex [[rating, jobURL]...]
    #Gives: rated and ranked jobIndex [[rating, jobURL]...]
    localIndex = []

    while len(jobIndex) > 0:
        flag = 0
        maxval = -10000
        for job in jobIndex:
            if job[0] >= maxval:
                maxval = job[0]
                tempjob = job
                flag = 1
        if flag == 1:
            localIndex.append(tempjob)
            jobIndex.remove(tempjob)
    return localIndex

#The Major Function
def jobSearch(agent, user, skills):
    #Takes: agent, user, skills from webpage call
    #Gives: Ranked Jobindex
    #Requires: All functions in this module
    #Uses all prior functions in order to recieve info from WebPage and give job results back to webpage
    jobIndex = getJobs(agent)
    skillIndex = userAttributesIndex(user)
    skillIndex += userSkillIndex(skills)
    jobIndex = rateJobs(skillIndex=skillIndex, jobIndex=jobIndex)
    jobIndex = rankJobs(jobIndex=jobIndex)
    return jobIndex




####################################################################
#
#
#           ON SITE TESTING ZONE
#
#   This will allow you to run the code by itself (assuming you have mechanize)
####################################################################


#DEFINE [ Name of the job you want, Location you want to work in ]
testAgent = ['Electrical Engineer', 'Burbank, CA']  #For Testing linkConstructor, and jobSearch

#DEFINE 'degree, minors, clases Taken, all that good stuff... put N/A if N/A'
class testUser:         #For Testing userAttributesIndex
    degree = 'Electrical Engineering, Mathematics'
    minors = 'Physics, Applied Mathematics'
    classesTaken = 'photonics, calculus, statistics, circuits, microcomputers, electromagnetic fields, electronic devices'
    personalTraits = 'Energetic, Enthusiastic, Ingenuitive'
    hobbies = '3D printing, hiking, coding, meditation'


#DEFINE     x.strengthLevel = int
#           x.skills 'comma sepperated string of skills'
#   You can add a,b,c,d... etc in addition to x, y, z

class skills:       #For Testing userSkillIndex
    strengthLevel = 0
    skills = ''
#Initialize
testSkills = []
x = skills()
y = skills()
z = skills()
x.strengthLevel = 1
x.skills = 'coding, matlab, c++, html, c , microcontrollers, vagrant'
y.strengthLevel = 3
y.skills = 'project management, labview, CAD'
z.strengthLevel = 5
z.skills = 'Robotics, electronics, python'
testSkills.append(x)
testSkills.append(y)
testSkills.append(z)


#Run the main fucntion
jobs = jobSearch(testAgent, testUser, testSkills)
for job in jobs:
    print job
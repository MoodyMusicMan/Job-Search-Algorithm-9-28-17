
import time
from datetime import datetime

from Functions.jobRater import job_rater
from Functions.sortIndex import sort_index

writeTextPageName = "C:/Users/M0J0/Documents/FOJ_2017/Python/Job-Results/" + "Resorted" + "28.10.2017_19.23.23" +"_ML_Focus_2" +  ".txt"
writeTextPage = open(writeTextPageName, "w")
readTextPageName = "C:/Users/M0J0/Documents/FOJ_2017/Python/Job-Results/" + "Full-Text_" + "28.10.2017_19.23.23" + ".txt"
readTextPage = open(readTextPageName, "r")

keyword_list_master = []        #[[supers],[regulars]]
keyword_list = []               #[[value1, word1, word2, word3...][value2, word1, word2, word3]]
keyword_list_supers = []        #[[[ Appearence Threshold, points worth],[word1, word2, word3]], [[],[]], [[],[]]...] # Appears Threshold == if word is seen this many times or more

keyword_list = [
                                        # Any of these words present in a job listing will add the first element worth of points to a job result
                                        # The code converts all letters to case letters
                                        # Use root words where possible i.e. "prototy" catches all conjugations of Prototyping
                                        # The formating sucks for single letter words. i.e "C" will be found inside ant word with a c, unless you treat it specialy. This is a known bug
	[10,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware', 'plc'],
    #[10, 'control', 'electrical engineer', 'embedded sys', 'matlab', 'keras', 'Tensorflow', 'scikit learn', 'sklearn', 'canopen'],
    [10, 'control', 'keras', 'Tensorflow', 'scikit learn', 'sklearn', 'canopen'],

    [30, 'microcontroller', 'servo', 'mcu', 'prototy', 'eagle'],
	#[100, 'opencv', 'open cv', 'systems engineer']
    [100, 'opencv', 'open cv']
]

keyword_list_supers = [                 #2 or more appearances for the words from the first list will award a 1 time bonus 1000 points
                                        #Note, any combination of  words from each super group will count towards threshold\
	[[2,2000], ['jr','junior','entry level','new grad']],     #i.e. 1x 'entry level' + 1x 'new grad', or 2x 'entry level', etc
    #[[2,-2000], ['mechanical engineer']],
	#[[3,-2000], ['senior','Sr. ']],          #I am not experienced enough to apply for Sr. level positions.
    #[[2, -2000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms', 'masters' ]],
    #[[3, -1000], ['nurse', 'technician']],  # NO NURSING POSITIONS PLEASE!
    #[[2, -1000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms ']], #Comment a line our if you don't want to use it anymore
    [[1,-100000], ['5 years','5+ years', '6 years','6+ years', '7 years','7+ years', '8 years', '8+ years', '9 years','9+ years', '10 years', '10+ years']]

]

keyword_list_master.append(keyword_list_supers)
keyword_list_master.append(keyword_list)


index = []

readTextPage = readTextPage.read().split('TOPANGA')

# 1: link, 2: HTML, 3: name, 4: decimal, 5: score,
for jobResult in readTextPage:
    unrankedResult = jobResult.split('TOPANGO')[0:3]
    if len(unrankedResult) == 3 :
        if len(unrankedResult[1]) > 0:
            index.append(unrankedResult)

# Rate Jobs Based on Keywords

index = job_rater(index, keyword_list_master)
index = sort_index(index)

print("Next Phase")
for a in index:
    writeTextPage.write(str(a[3]) + ',' + str(a[4]) + ' : ' + a[0])  ##a[3] is type int, so needs to be forced str())
    writeTextPage.write('\n')

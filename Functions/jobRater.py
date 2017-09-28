__author__ = 'Jo'


import re

#Pass in:   List of Keywords to rate based on, and an index
            # where index[i][0]=sitelink, [i][1]=htmlinfo, [i][2]=job_name
#Returns:   an index with index[i][3]=Rating

    #This is where I think the DQ logic would be appropriate...
    #There is depricated DQ logic included at the bottom of this function

def job_rater(indexz,keyword_master):

	super_key = keyword_master[0]           #Split in to super words
	keywordz = keyword_master[1]            # and 'points per word' words

	i = 0
	while i < len(indexz):

		ranks = 0
		count = 0
		sups_count = 0

		while sups_count < len(super_key):

			combo_break = super_key[sups_count][0][0]       #Number of times word needs to occur
			limit_break = super_key[sups_count][0][1]       #Number of points awarded if combo achieved
			total_entry_number = 0

			for entry in super_key[sups_count][1]:
				match = re.findall(entry.lower(),indexz[i][1].lower())
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

		count2 = float(count) / len(indexz[i][1]) 	#Modifying For Demonstration Purposes
		indexz[i].append(count2)
		indexz[i].append(count)
		i+=1


	return indexz


#--------------------------------------------DEPRICATED-------------------------------

#This was in the main function orriginally
    #Also sing string.tolower() on our htmltext and keyword lists makes some of these repeats not necessary
"""
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

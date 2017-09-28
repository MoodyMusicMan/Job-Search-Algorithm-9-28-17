__author__ = 'Jo'



#Pass in: an Unsorted Index
#Returns: an Sorted Index
    #Something might be loopy with this logic... Some jobs are returned multiple times...
    #It looks solid to me though...


def sort_index(jobIndex):
#Takes: rated jobIndex [[rating, jobURL]...]
    #Gives: rated and ranked jobIndex [[rating, jobURL]...]
    localIndex = []

    while len(jobIndex) > 0:
        flag = 0
        maxval = -10000
        for job in jobIndex:
            if job[4] >= maxval:
                maxval = job[4]
                tempjob = job
                flag = 1
        if flag == 1:
			if tempjob not in localIndex:
				localIndex.append(tempjob)
			jobIndex.remove(tempjob)



    return localIndex

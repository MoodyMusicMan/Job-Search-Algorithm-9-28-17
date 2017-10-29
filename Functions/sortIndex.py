__author__ = 'Jo'



#Pass in: an Unsorted Index
#Returns: an Sorted Index


def sort_index(jobIndex):
#Takes: rated jobIndex [[rating, jobURL]...]
    #Gives: rated and ranked jobIndex [[rating, jobURL]...]
    localIndex = []
    weblink_index = []

    while len(jobIndex) > 0:
        flag = 0
        maxval = -10000000000000000
        for job in jobIndex:
            if job[4] >= maxval:
                maxval = job[4]
                tempjob = job
                flag = 1
        if flag == 1:
            if tempjob[0] not in weblink_index and tempjob[0][-4:] != 'rm=1' and tempjob[0][-11:] != 'job-content':
                weblink_index.append(tempjob[0])
                localIndex.append(tempjob)
            jobIndex.remove(tempjob)




    return localIndex

__author__ = 'Jo'


keywords = [

	[1,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware','prototy'],
	[10, 'control', 'electrical engineer', 'matlab', 'servo'],
	[30, 'plc', 'microcontroller'],
	[100, 'lab view', 'labview']
]


i1 = 0
while i1 <  len(keywords):
    strength = keywords[i1][0]

    #itterate through keywords, replace them to root
    i2 = 0
    while i2 < len(keywords[i1])-1:
        keywords[i1][i2+1] = keywords[i1][i2+1].replace('p','')
        i2+=1
    i1+=1

for line in keywords:
    print line

__author__ = 'Jo'

from getTargetData import get_target_data


#Pass in: Pattern of name/title to be found, an index with index[i][0]=sitelink, [i][1]=htmlinfo
#Returns: an index where index[i][2]=job_name


def get_title(name_style, indexz):

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
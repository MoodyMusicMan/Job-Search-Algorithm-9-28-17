import time
from datetime import datetime

from Functions.fillIndex import fill_index
from Functions.getTitle import get_title
from Functions.getWebpage import get_webpage
from Functions.jobRater import job_rater
from Functions.sortIndex import sort_index
from Functions.getTargetData import get_target_data
from Functions.makeFullLink import make_full_link


website = "https://www.indeed.com/jobs?q=Robotics+Engineer&l=Miami%2C+FL"
link_style = '<h2 id=[^.?]* class="jobtitle">[^.?]*href="(.+?)"' # Had to add the ? to the s>[^.?] in order to make it non-greedy. Previously it was attempting to grab all of the data between the most amount of matching syntax it could find.. Interesting resutls.
link_style = 'Jobs[^.?]*of (.+?)</div>'    #Pattern of "Total number of jobs" result=


#link_style = 'href="(.+?)" target="_blank" rel="noopener nofollow'
#link_style2 = 'href="/company(.*?)"'
#link_style = 'href="/rc(.*?)"'


#'href="(.+?)"'
text = get_webpage(website)
links = get_target_data(link_style, text)
#print text

for link in links: print(link)

'''
/cmp/Stryker
/rc/clk?jk=fb2b69bb4bdefd70&fccid=250b3b23ab6d1a65
/cmp/Stryker
/company/National-Molding,-LLC/jobs/Senior-Process-Engineer-e34f55fc95439637?fccid=e6790b2a5e5d4e31
/cmp/Magic-Leap
/cmp/Stryker
/cmp/Magic-Leap
/rc/clk?jk=9c3e9f16dfb2654f&fccid=7847eeddd5ec77ae
/company/DBP-ROBOTICS/jobs/Coach-Robotic-Electronic-Kids-2c26d2088bb43e64?fccid=6c0fef4e641a75e8
/cmp/Stryker


<h2 id=jl_fb2b69bb4bdefd70 class="jobtitle">
    <a
                                               href="/rc/clk?jk=fb2b69bb4bdefd70&fccid=250b3b23ab6d1a65" target="_blank" rel="noopener nofollow"
                                               onmousedown="return rclk(this,jobmap[1],0);"
                                               onclick="setRefineByCookie([]); return rclk(this,jobmap[1],true,0);"
                                               title="Sr. Product Quality Engineer"
                                               class="turnstileLink"
                                               data-tn-element="jobTitle">Sr. Product Quality <b>Engineer</b></a>
                                               
                                               
<h2 id=jl_efdc996b670b2d83 class="jobtitle">
    <a
                                               href="/rc/clk?jk=efdc996b670b2d83&fccid=7847eeddd5ec77ae" target="_blank" rel="noopener nofollow"
                                               onmousedown="return rclk(this,jobmap[0],0);"
                                               onclick="setRefineByCookie([]); return rclk(this,jobmap[0],true,0);"
                                               title="Surgical Robotics Application Software Engineer"
                                               class="turnstileLink"
                                               data-tn-element="jobTitle">Surgical <b>Robotics</b> Application Software <b>Engineer</b></a>
<h2 id=jl_e34f55fc95439637 class="jobtitle">
    <a
                                               href="/company/National-Molding,-LLC/jobs/Senior-Process-Engineer-e34f55fc95439637?fccid=e6790b2a5e5d4e31" target="_blank" rel="noopener nofollow"
                                               onmousedown="return rclk(this,jobmap[3],0);"
                                               onclick="setRefineByCookie([]); return rclk(this,jobmap[3],true,0);"
                                               title="Senior Process Engineer"
                                               class="turnstileLink"
                                               data-tn-element="jobTitle">Senior Process <b>Engineer</b></a>

'''
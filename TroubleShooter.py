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


text = get_webpage(website)

print text
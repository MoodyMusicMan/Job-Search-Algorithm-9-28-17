# Read Me Slightly out of date. Check code for more up-to-date info.
## Main file has all the information

# JobSearch
#### This is a program designed to aid in the acquisition of employment by targeting jobs based on skills of the user.


## What Does it Do?
--- The program currently takes in a target job title or field of interest and a geographical location, and scrolls indeed.com to look for jobs of that type. It then ranks those jobs based on a keyword list that you define in the program. ---
--- Please define keywords in the program that reflect skills you want to work with, or words that resonate with the culture you would like to participate in. ---
--- an example of skills you want to work with would be 'arduino', while an example of culture would be the word "awesome". You can tell a bit about a culture by the types and frequency of words used in a job description. ---

## Requirements:
#### You must have the following
---Python version 2.7 (might work on python 3, however, might have bugs!). Check online for how to install Python 2.7---
---Mechanize library for python (You can PIP install using, "$ pip install mechanize"). Check online for how to install PIP---
---A destination folder to store your results in. (Make sure you have permission to write files in whichever directory the program is in


## How To Use:
--- Check the Main.py file, and set four major sections:
--- 1. (Line 18) Initial Conditions. Change url part 2 and url part 3 to match your Desired Job Field, and your Desired Job Location respectively. You have to acquire these by going to indeed.com and typing in your desired job title and location, and then cutting the url returned up to match the code.
--- 2. (Line 30) Define a Directory to store your output text file in.
--- 2. (Line 45) Key Words : keyword_list - These are the keywords that will be used to rank your returned job results. Change the integer numbers in each column to match how important a skill is to you in the keyword_list. This list will award a point for every time a word shows up in the job posting. i.e. if you REALLY like arduinos, put it in the 100 points column. You can define new columns by matching the format of the provided example list. Any integers are acceptable in the first column of each list, any number of skills can be added to each column, and any number of columns can be added to keywords_list.
--- 3. (Line 45 )Key Words : keyword_list_supers - These are groups of words that will trigger bonus points if any of the words (or combination) shows up more than a specified threshold. i.e. [[2,1000], ['Jr','Junior','entry level','new grad']]," will trigger 1000 bonus points if 1x 'entry level' + 1x 'new grad', or 2x 'entry level', etc occurs in a job listing.

## Results File:
--- If you want to modify the results format, please do so! ---
--- Currently the results file displays the averaged job listing score (total score / number of characters in listing) followed by the total score, followed by the web link to that listing.
--- Very no-frills, but could use some work.


## If you run into trouble:
--- post on here, or send me an email at john.moody@ieee.org ---

### Happy Hunting!

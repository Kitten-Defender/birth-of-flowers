### Quick little script to see
# how many fucking dungeon slaves MegaMatt has to keep his fanfic output
# Surprisingly, the answer is "none".
# He just doesn't have a life
# –Samantha V. Bookholder

from bs4 import BeautifulSoup
import requests
import re
from datetime import date
from time import sleep

###~~~~~~~~~~~~~~~~~~~~WEB SCRAPER~~~~~~~~~~~~~~~~~~~~###

#url = ask("Please enter the user number of the author") ¿¿¿Add customization options later???
url = "http://www.fanfiction.net/u/424665/"


# opens the url in BS
http = requests.get(url)
page = BeautifulSoup(http.text, 'html.parser')

# makes a list of all the fanfic characteristics
wordcounts = page.find_all(class_="z-padtop2")
running = 0

#Truncates each to get out everything but the wordcounts
for m in wordcounts:
    # searches for "Words:" followed by an arbitray number of digits
    k = re.search(r"Words:\s\d+,?\d+,?\d+", str(m))
    if k:
        #sets a var equal to what the regex search found, truancates it and adds it to the running total
        words = k.group(0)
        words = words.replace("Words: ", "")
        words = words.replace(",", "")
        words = int(words)
        running = running + words
    else:
        print("Oh No! Something went wrong!")
        

###~~~~~~~~~~~~~~~~~~~~UI + MATH~~~~~~~~~~~~~~~~~~~~###

# Type out text
def write(text):
    i = 0
    while i < len(text):
        if text[i-1] in [".", "\n"]:
            sleep(0.2)
            print(text[i], end="", flush=True)
        elif text[i-1] in [";",",",":","—"]:
            sleep(0.1)
            print(text[i], end="", flush=True)
        else:
            sleep(0.03)
            print(text[i], end="", flush=True)            
        i += 1
        
def ask(text):
    write(text)
    x = intmaker(input("\n"))
    return x
        
        
#function to get rid of commas
def intmaker(x):
     x = x.replace(",","")
     if "." in x:
         x = float(x)
     else:
         x = int(x)
     return x
    
write("""The fanfiction author known as MegaMatt09 is a longtime internet mystery.
He has an absolutely massive output of works, an output that would seemingly
require a dedicated full-time writer, and not just the hobbyist that he is.\n""")
sleep(1)
write("""So I decided to solve this mystery: how much does MegaMatt write per day,
and how long would YOU have to work to write that much?\n""")

write("Enjoy.\n\n\n")

sleep(2)

#gets variables
hours_per_day = ask("How many hours per day will you write?")
if hours_per_day > 24:
    hours_per_day = ask("A day only has 24 hours. Let's try entering that again, Einstein.\n")
if hours_per_day < 1:
        hours_per_day = ask("A day has at least one hour, dude.\n")
    
words_per_day = ask(f"On average, how many words will you write in those {hours_per_day} hours?")
    
days_per_week = ask("How many days per week will you write?")
if days_per_week > 7:
    days_per_week = ask("A week only has 7 days. Do better this time.\n")
if days_per_week < 1:
    days_per_week = ask("A week has at least one day. That's how numbers work, you absolute moron.\n")
    
wpm = ask("How many words per minute do you write at your fastest?\nThe average speed is 39 when copying something.")


# Do the math on how much you need to write to match Matt
def calc(wpm_loc, hours_per_day_loc, words_per_day_loc, days_per_week_loc):
    copy = round(((running / wpm_loc) / 60) / hours_per_day_loc) # Total days to copy
    days = round(running / words_per_day_loc) # Total days to write
    hrs = round((days * hours_per_day_loc))
    yrs = round((days / days_per_week_loc) / 52) # Total Years
    mon_rem = round(((days / days_per_week_loc) % 52) / 12) # How many months remaining in the partial year
    return hrs, days, yrs, mon_rem, copy


#The day MegaMatt started seriously writing with his insane pace. The "dungeon era".
#He wrote 1,085,777 words before that, at a much, MUCH slower pace.
running1 = running - 1085777

def careercalc():
    the_day_it_began = date(2012,8,18)
    today = date.today()
    career_days = round((today - the_day_it_began).days) #the total number of days he's been writing
    words_per_day_loc = round(running1 / career_days)
    career_years = round(career_days / 365)
    career_rem_mon = round(career_days / 30.42 % 12)
    return words_per_day_loc, career_years, career_rem_mon

hrs,days,yrs,mon_rem,copy = calc(wpm, hours_per_day, words_per_day, days_per_week)
c_words_per_day,c_yrs,c_mon_rem = careercalc()


#All the functions for the grammar-correcting if/then trees
def finale(): # This is the main one!
    output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years and {mon_rem:,} months (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years and {c_mon_rem} months, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
    return output
    
def nomonth1(): # if the months of the first y/m pair returns zero
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years and {c_mon_rem} months, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output
    
def nomonth2(): # if the months of the second y/m pair returns zero
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years and {mon_rem:,} months (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output

def nomonthboth(): #if both pairs return zero
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output
    
def onemonth1():# if the first y/m pair returns one
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years and 1 month (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years and {c_mon_rem} months, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output
    
def onemonth2(): #if the second one returns one
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years and {mon_rem:,} months (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years and 1 month, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output
    
def onemonthboth(): #if both return one
        output = (f"MegaMatt09 has written {running:,} words of fanfiction in total.\n" 
            f"At the rate you indicated, it would take you {yrs:,} years and 1 month (that's {days:,} days, or {hrs:,} hours)\n" 
            f"to completely match his output of written work. It would take you {copy:,} days just to copy it out.\n" 
            f"Matt has been writing at his insane pace for {c_yrs} years and 1 month, since July 2012\n"
            f"Working every day of the year, he'd need to have written {c_words_per_day:,} words per day in order to reach his current output.\n"
            f"Godspeed, you bizarre little writing troll.")
        return output


if mon_rem == 0:
    if c_mon_rem == 0:
        output = nomonthboth()
    else:
        output = nomonth1() 
elif c_mon_rem == 0:
    output = nomonth2()
elif mon_rem == 1:
    if c_mon_rem == 1:
        output = onemonthboth()
    else:
       output = onemonth1()
elif c_mon_rem == 1:
    output = onemonth2()
else:
    output = finale()

write(output)

input("")
## FFNet Archive Searcher 2.0
## Work in Progress
## Creator: Samantha Ravenwood (kitten-defender on github)

import bs4 as bs
import requests
import re
from tqdm import tqdm

##searches through FFnet communities for a key word
class FFNet:
    
    #finds the pagecount of the archive
    #literally just uses regex to find whatever is after 'Last: " because FFNet's HTML is TERRIBLE
    def pagecount(self, url):
        http = requests.get(url)
        page = bs.BeautifulSoup(http.text, 'html.parser')
        lastTxt = page.find(text="Last")
        last = str(lastTxt.find_parent("a"))
        max_pagecount = re.findall("(?<=\/)[^\/]*", last)[5]
        return int(max_pagecount)

    #returns a list of the urls of all the pages in the archive
    def iterate_url(self,url):
        pc = self.pagecount(url)
        
        #divides the url into blocks (chapter count is 7th)
        url = url.replace("https://","")
        url = url.replace("http://","")
        urlements = re.findall("[^\/]+", url)

        #creates a list of the urls for every page
        urls = []
        for i in range(1,(pc+1)):
            newrlist = urlements #replaces the pagecount with i
            newrlist[6] = str(i)
            newrl = "/".join(newrlist)
            newrl = "http://" + newrl
            urls.append(newrl)
        return urls
    
    #returns a list of all the stories in the community
    def storyget(self, url):
        links = self.iterate_url(url)
        #for each page of the community
        pages = []
        for i in tqdm(range(len(links))):
            link = links[i]
            # opens the url in BS
            http = requests.get(link)
            page = bs.BeautifulSoup(http.text, 'html.parser')
            
            #gets stories for page
            stories_loc = page.find_all(class_="z-list")
            pages.append(stories_loc)
        while len(pages) > 1:
            pages[0].extend(pages[1])
            pages.remove(pages[1])
        
        stories = pages[0]
        return stories

    #function to return the individual parts of a story
    def get(self, story, part):
        part = part.lower()
        if part == "title":
            return story.find(class_= "stitle").getText()
        elif part == "fandom":
            info = story.find(class_= "z-padtop2 xgray").getText()  #the bit on the bottom with all the info
            info = info.split(" -")
            match = info[0]   #gets item before first "-" divider
            if "Crossover" in match:
                return info[1][1:]  #If crossover, returns the actual crossover fandoms
            else:
                return match
        elif part == "chars":
            return story.find(class_= "z-padtop2 xgray").getText()
        elif part == "author":
            return story.find(href=re.compile("\/u\/")).getText() #gets text of the tag with a link with "/u/" in it
        elif part == "desc":
            return str(story.find(class_= "z-indent z-padtop").contents[0])
        elif part == "words":
            info = story.find(class_= "z-padtop2 xgray").getText()
            info = re.findall("(?<=Words: )[^- ]+", info) #everything between "Words: " and " -"
            info = info[0]
            return int(re.sub("[^\d]", "",info)) #takes out all non-digits
    
    def assemble(self, story):
        title = self.get(story, "title")
        author = self.get(story,"author")
        desc = self.get(story, "desc")
        fandom = self.get(story, "fandom")
        words = self.get(story, "words")
        print(f"""{title}\nBy: {author}\n{fandom}\n{words:,} words\n{desc}\n\n""")

    def search(self, cat, term, url):
        stories = self.storyget(url)
        if cat == "words": #words are a sepcial case bc you're comparing ints, not searching strings
            if "<" in term:
                sign = "<"
                term = term.replace("<", "")
                term = int(re.sub("[^\d]", "",term))
                for story in stories:
                    if self.get(story, "words") <= term:
                        self.assemble(story)
                        
            elif ">" in term:
                sign = ">"
                term = term.replace(">", "")
                term = int(re.sub("[^\d]", "",term))
                for story in stories:
                    if self.get(story, "words") >= term:
                        self.assemble(story)
            elif "=" in term:
                sign = "="
                term = term.replace("=", "")
                term = int(re.sub("[^\d]", "",term))
                for story in stories:
                    if self.get(story, "words") == term:
                        self.assemble(story)
            else:
                print("Incorrect format for words!")
            
        else:
            if " OR " in term:
                term = term.split(" OR ")  # allows for multiple terms
                for story in stories:
                    for subterm in term:
                        if subterm.lower() in self.get(story, cat).lower():
                            self.assemble(story)
            else:    #single-term search
                for story in stories:
                    if term.lower() in self.get(story, cat).lower():
                        self.assemble(story)



ffn = FFNet()

url = input("Enter community URL:\n")

print("Options:\n 'f': fandom\n 's': summary \n 'c': characters\n 'a': author\n 't': title\n 'w': words")


#lays out the choices
#I'm using a while loop to enable re-tries if the choice doesn't exist
while True:
    q1 = input("Choice: ").lower()
    if q1 == "f":
        term = input("Enter Fandom: ")
        stories = ffn.search("fandom", term, url)
        break
    elif  q1 == "s":
        term = input("Enter term to search in summary: ")
        stories = ffn.search("desc", term, url)
        break
    elif q1 == "c":
        term = input("Enter characters: ")
        stories = ffn.search("chars", term, url)
        break
    elif q1 == "a":
        term = input("Enter author: ")
        stories = ffn.search("author", term, url)
        break
    elif q1 == "a":
        term = input("Enter author: ")
        stories = ffn.search("author", term, url)
        break
    elif q1 == "t":
        term = input("Enter title: ")
        stories = ffn.search("title", term, url)
        break
    elif q1 == "w":
        term = input("Enter words using <, >, or =: ")
        if "<" not in term and ">" not in term and "=" not in term:
            print("Please enter your wordcount correctly:")
        else:
            stories = ffn.search("words", term, url)
            break
    else:
        print("Enter a valid search term!")
        continue
    
input("Done")

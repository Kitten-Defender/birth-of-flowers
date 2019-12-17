## FFNet Archive Searcher 1.0
## Work in Progress
## Creator: Samantha Ravenwood (kitten-defender on github)

import bs4 as bs
import requests
import re
from tqdm import tqdm

##searches through FFnet communities for a key word
class FFNet:
    def pagecount(self, url):
        http = requests.get(url)
        page = bs.BeautifulSoup(http.text, 'html.parser')
        lastTxt = page.find(text="Last")
        last = str(lastTxt.find_parent("a"))
        max_pagecount = re.findall("(?<=\/)[^\/]*", last)[5]
        return int(max_pagecount)

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

    
    def get(self, story, part):
        part = part.lower()
        if part == "title":
            return story.find(class_= "stitle").getText()
        elif part == "fandom":
            info = story.find(class_= "z-padtop2 xgray").getText()
            info = re.findall("[^-]+(?= -)", info) #gets item before first "-" divider
            match = info[0]
            if "Crossover" in match:
                return info[1][1:]  #If crossover, returns the actual crossover fandoms
            else:
                return match
        elif part == "author":
            return story.find(href=re.compile("\/u\/")).getText() #gets text of the tag with a link with "/u/" in it
        elif part == "desc":
            return str(story.find(class_= "z-indent z-padtop").contents[0])
    
    def assemble(self, story):
        title = self.get(story, "title")
        author = self.get(story,"author")
        desc = self.get(story, "desc")
        fandom = self.get(story, "fandom")
        print(f"{title}\nBy: {author}\n{fandom}\n{desc}\n\n")

    def subsearch(self, cat, term, url):
        stories = self.storyget(url)
        if " OR " in term:
            term = term.split(" OR ")
            for story in stories:
                for subterm in term:
                    if subterm.lower() in self.get(story, cat).lower():
                        self.assemble(story)
        else:
            for story in stories:
                if term.lower() in self.get(story, "fandom").lower():
                    self.assemble(story)
    
    def search(self, cat, term, url):
        if cat == "fandom":
            self.subsearch("fandom", term, url)
        elif cat == "desc" or cat == "description" or cat == "summary":
            self.subsearch("desc", term, url)
        else:
            print("ERROR!!!! INVALID CATEGORY!!!!")


ffn = FFNet()

url = input("Enter community URL\n")

q1 = input("Enter 'f' for fandom or s for summary: ").lower()

if q1 == "f":
    fandom = input("Enter Fandom: ")
    stories = ffn.search("fandom", fandom, url)
elif  q1 == "s":
    summ = input("Enter term to search in summary: ")
    stories = ffn.search("desc", summ, url)
else:
    print("Enter valid search term.")
    
print("\n")

input("\nDone")


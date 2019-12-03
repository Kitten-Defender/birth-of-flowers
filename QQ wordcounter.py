## Made by Sam Ravenwood


import bs4 as bs
import requests
import re
from tqdm import tqdm

#creates a list of the urls of every page
def iterate(url):
    http = requests.get(url)
    page = bs.BeautifulSoup(http.text, 'html.parser')
    #finds max pagecount
    pagecount = int(page.find(text="Next >").previous_element.previous_element.previous_element)
    if url[len(url)-1] == "/":
        url = url + "page-"
    else:
        url = url + "/page-"
    links = []
    for i in range(1, pagecount+1):
        links.append(url + str(i))
    return links

def get(cat, url):
    assert cat in ["posts","title"], "Incorrect category for get request!"
    http = requests.get(url)
    page = bs.BeautifulSoup(http.text, 'html.parser')
    if cat == "posts":
        return page.find_all(class_="message")
    if cat == "title":
        return page.find("title").get_text().replace(" | Questionable Questing", "")

def counter(msg):
    msg = str(msg)
    msg = re.sub("[^a-zA-Z0-9_\s]", "",msg) #deletes all characters that aren't alphanumeric or a space
    msg = msg.split(" ")
    return len(msg) + 1

#creates a list of every message in the thread
def wordcount(url):
    links = iterate(url)
    total = 0
    #for each page of the community, get wordcount of each post, add it to total
    for i in tqdm(range(len(links))):  #for each page
        link = links[i]
        posts_loc = get("posts", link)
        for post_loc in posts_loc: #for each post in page
            count = counter(post_loc.get_text())
            total += count
    
    return total

        

url = input("Enter url:\n")
if "http://" not in url and "https://" not in url:
    url = "https://" + url

print("Analyzing pages...")
print(f"\nThread '{get('title', url)}' has total wordcount of {wordcount(url):,} words.")
input()
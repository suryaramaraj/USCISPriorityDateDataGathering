from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re
import pandas as pd
import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
for n in range(64,-1,-1):
    url = 'https://www.uscis.gov/green-card/green-card-processes-and-procedures/visa-availability-priority-dates/when-to-file-your-adjustment-of-status-application-for-family-sponsored-or-employment-based-'+str(n)
    html = urllib.request.urlopen(url).read()
    allcontent = text_from_html(html)

    date = re.search('Employment-Based Preference Visas:(.+?)When',allcontent).group(1)
    r = requests.get(url)
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[0]
    count = 0
    for d in df_list:
        if 'Employment- Based' in d or 'Employment-Based' in d:
            count=count+1
            df = d
    if count>1:
        print("Has two tables");
    col = 'INDIA' if 'INDIA' in df else 'India'
    row = 'Employment- Based' if 'Employment- Based' in df else 'Employment-Based'
    priorityDate = df[col].values[df[row] == '3rd']
    type = 'Final Action Date' if 'Final Action Dates for Employment-Based Adjustment of Status Applications' in r.text or 'Final Action Dates for Employment-Based Adjustment of Status Applications' in r.text else 'File Date'
    print(date,type,  priorityDate , url)

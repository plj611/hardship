import pandas
import requests
from bs4 import BeautifulSoup

#compdb = pandas.read_excel('.\compdb.xlsx','name1')
url = 'https://zh.wikipedia.org/api/rest_v1/page/html/YUSEI'

re = requests.get(url)

soup = BeautifulSoup(re.text, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

lines = (line.strip() for line in text.splitlines())

# remove empty lines
lines1 = (l for l in lines if l)

print(lines1)

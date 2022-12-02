import pandas
import requests
import sys
from bs4 import BeautifulSoup

compdb = pandas.read_excel('./compDB.xlsx', sys.argv[1])

if sys.argv[2] != 'check':
   df = pandas.DataFrame({'code':[], 'company':[], 'description':[]})

for c, n in zip(compdb['name2'].tolist(), compdb['number'].tolist()):
   url = f'https://zh.wikipedia.org/api/rest_v1/page/html/{c}'

   re = requests.get(url)

   print(f'Retrieving {n} - {c}')

   if re.status_code != 404 and sys.argv[2] != 'check':
      soup = BeautifulSoup(re.text, features="html.parser")

      # kill all script and style elements
      for script in soup(["script", "style"]):
         script.extract()    # rip it out

      # get text
      text = soup.get_text()

      lines = (line.strip() for line in text.splitlines())

      # remove empty lines
      lines1 = (l for l in lines if l)

      while True:
         try:
            l = next(lines1)
            a = len(l)
            while a < 250:
               l += next(lines1)
               a = len(l) 
         except StopIteration:
            break
         #print('3', l, len(l))
         df = pandas.concat([df, pandas.DataFrame({'code': n, 'company': c, 'description': l}, index=[1])], ignore_index=True)
      #print('3', l, len(l))
      df = pandas.concat([df, pandas.DataFrame({'code': n, 'company': c, 'description': l}, index=[1])], ignore_index=True)
      re.close()
   else:
      if sys.argv[2] == 'check':
         if re.status_code == 404:
            print(f'{n} - {c}')
      else:
         df = pandas.concat([df, pandas.DataFrame({'code': n, 'company': c, 'description': 'No information'}, index=[1])], ignore_index=True)

if sys.argv[2] != 'check':
   df.to_excel('./a.xlsx', sheet_name = sys.argv[1], index=False)
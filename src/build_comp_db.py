import pandas
import requests
from bs4 import BeautifulSoup

compdb = pandas.read_excel('./compDB.xlsx','1-99')
df = pandas.DataFrame({'code':[],
                        'description':[]})

for c, n in zip(compdb['name2'].tolist(), compdb['number'].tolist()):
   url = f'https://zh.wikipedia.org/api/rest_v1/page/html/{c}'

   re = requests.get(url)

   if re.status_code != 404:
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
         df = pandas.concat([df, pandas.DataFrame({'code': n, 'description': l}, index=[1])], ignore_index=True)
      #print('3', l, len(l))
      df = pandas.concat([df, pandas.DataFrame({'code': n, 'description': l}, index=[1])], ignore_index=True)
      re.close()
   else:
      #print(c, n)
      print(df)
df.to_excel('./a.xlsx')
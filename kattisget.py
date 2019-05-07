#!/usr/bin/python3
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
import os





# Because the methodstosolve thing has an expired ssl certificate.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if(len(sys.argv) < 2):
  print('Use: kattisget <problemid> (<py>)'.format(sys.argv[0]))
  exit()


cppInit = """#include <bits/stdc++.h>
using namespace std;

int main(){

  return 0;
}
"""

pythonTemplate = '''
print('IMPLEMENT ME')
'''




usePy=False
if(len(sys.argv)==3):
  if sys.argv[2] == 'py':
    usePy = True


def get_hints(id):
  url = 'https://cpbook.net/methodstosolve'
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.text, "html.parser")
  pres = [s.find_all('tr') for s in soup.find_all('table', id='problemtable')][0][1:]
  for x in pres:
    title = x.find_all('td')[0].get_text()
    hint = x.find_all('td')[3].get_text()

    if title == id:
      return hint

  return 'no hint found'

if __name__ == '__main__':
  url = 'https://open.kattis.com/search?q='+sys.argv[1]
  response = requests.get(url)
  if "search" in response.url:
    print("please write the exact problem id")
    sys.exit()


  problemId = response.url.split('/')[-1]
  problemDir = './'+problemId
  
  problemPath = problemDir+"/"+problemId+".cpp" if not usePy else problemDir + '/' + problemId + '.py'

  if not os.path.exists(problemDir):
    os.mkdir(problemDir)
  if not os.path.exists(problemPath):
    with open(problemPath, 'w') as f:
      if usePy:
        f.write(pythonTemplate)
      else:
        f.write(cppInit)

  soup = BeautifulSoup(response.text, "html.parser")
  pres = [s.find_all('pre') for s in soup.find_all('table', class_='sample')]
  tcs = []
  for x in pres:
    tcs.extend(x)
  tcs = [s.text.replace('<pre>','') for s in tcs]
  tcs = [s.replace('</pre>','') for s in tcs]

  for k in range(0, len(tcs), 2):
      with open(problemDir+'/in'+str(k+1)+".txt", 'w') as f:
        f.write(tcs[k])
      with open(problemDir+'/out'+str(k+1)+".txt", 'w') as f:
        f.write(tcs[k+1])
  
  if not usePy:
    makeInit = "compile:\n\tg++ -std=c++17 -Wall -static -O2 {0} -o run.out\ntest:\n\tg++ -std=c++17 -Wall -static -O2 {0} -o run.out".format(problemId+".cpp")
    for k in range(0,len(tcs),2):
      makeInit += "\n\t./run.out < in{}.txt > temp".format(k+1)
      makeInit += "\n\tdiff -y out{}.txt temp".format(k+1)
      
  else:
    makeInit = "test:\n"
    for k in range(0, len(tcs), 2):
      makeInit += "\n\tpython {}.py  < in{}.txt > temp".format(problemId ,k+1)
      makeInit += "\n\tdiff -y out{}.txt temp".format(k+1)



  with open(problemDir+'/makefile', 'w') as f:
    f.write(makeInit)

  print('Done creating directory, fetching hint')
  print(get_hints('\033[95m'+sys.argv[1])+'\033[0m')


#!/usr/bin/python3
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
import os

cppInit = """#include <bits/stdc++.h>
using namespace std;

int main(){

  return 0;
}
"""


if __name__ == '__main__':
  url = 'https://open.kattis.com/search?q='+sys.argv[1]
  response = requests.get(url)
  if "search" in response.url:
    print("please write the exact problem id")
    sys.exit()
  problemId = response.url.split('/')[-1]
  problemDir = './'+problemId
  problemPath = problemDir+"/"+problemId+".cpp"
  if not os.path.exists(problemDir):
    os.mkdir(problemDir)
  if not os.path.exists(problemPath):
    with open(problemPath, 'w') as f:
      f.write(cppInit)

  soup = BeautifulSoup(response.text, "html.parser")
  pres = [s.find_all('pre') for s in soup.find_all('table', class_='sample')]
  tcs = []
  for x in pres:
    tcs.extend(x)
  tcs = [s.text.replace('<pre>','') for s in tcs]
  tcs = [s.replace('</pre>','') for s in tcs]
  tccount = 1

  makeInit = "compile:\n\tg++ -std=c++17 -Wall -static -O2 {0} -o run.out\ntest:\n\tg++ -std=c++17 -Wall -static -O2 {0} -o run.out".format(problemId+".cpp")
  for k in range(0,len(tcs),2):
    with open(problemDir+'/in'+str(tccount)+".txt", 'w') as f:
      f.write(tcs[k])
    with open(problemDir+'/out'+str(tccount)+".txt", 'w') as f:
      f.write(tcs[k+1])
    makeInit += "\n\t./run.out < in{}.txt > temp".format(tccount)
    makeInit += "\n\tdiff out{}.txt temp".format(tccount)
    tccount += 1
  with open(problemDir+'/makefile', 'w') as f:
    f.write(makeInit)

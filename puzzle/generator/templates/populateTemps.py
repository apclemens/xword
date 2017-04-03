import urllib2
from addTemplate import *
import math

def getYearURLs(year):
  url = 'http://www.xwordinfo.com/Calendar/%d'%year
  page = urllib2.urlopen(url)
  html = page.read()
  dates = ['http://www.xwordinfo.com/Crossword?date=' + A.split('"')[0] for A in html.split('data-date="')][1:]
  return sorted(list(set(dates)))

def tempFromURL(url):
  print url
  page = urllib2.urlopen(url)
  html = page.read()
  htmlTable = html.split('id="PuzTable"')[1].split('</table>')[0]
  htmlCells = htmlTable.split('</td>')[:-1]
  template = ''.join([' ' if 'class="black"' in c else '*' for c in htmlCells])
  return template

def addYear(yr):
  urls = getYearURLs(yr)
  templates = [tempFromURL(url) for url in urls]
  for temp in templates:
    size = int(math.sqrt(len(temp)))
    addTemplate(size, temp)

def main():
  for yr in range(1998, 2017):
    addYear(yr)

if __name__ == '__main__':
  main()
  

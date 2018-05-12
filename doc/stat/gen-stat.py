#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

# apt-get install python-bs4 python-requests imagemagick

PREFIX = "www.innovatefpga.com/cgi-bin/innovate/teams.pl?Id="

import os

import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

import requests

class teaminfo:

    def __init__(self, team, category, leader, org, update, img, title, videohref, mdgit, darch):

        self.team = team

        self.category = category
        self.leader = leader
        self.org = org
        self.update = update
        self.img = img
        self.title = title

        self.videohref = videohref
        self.mdgit = mdgit
        self.darch = darch


def parse_one(url):

    #resp = requests.get(url)
    #s = resp.text
    #soup = BeautifulSoup(s.encode('utf-8'), "lxml")

    #print(filename)
    with open(filename) as fp:
        s = fp.read()
        soup = BeautifulSoup(s.encode('utf-8'), "lxml")

    #print(soup.prettify())

    i = soup.find('div', {'class': " one-fourth"})
    j = i.find('div', {'style': "margin:10px 0px;padding-left:10px;"})
    k = j.find('div')
    l = k.find('a')
    team = None
    title = None
    team_title = l.get_text().encode('utf-8')
    team, title = team_title.split(" »")
    title = title.strip()

    i = soup.find('div', {'class': " three-fourths"})
    j = i.find('div', {'class': "ProjectImage"})
    k = j.find('img')
    img = k['src']

    h = soup.find('small')

    [s.decompose() for s in h('span')]

    data = str(h)
    data = data.replace('\n', '')
    data = data.replace('<small>', '')
    data = data.replace('</small>', '')
    data = data.split('<br/>')

    category = data[0]
    leader = data[1]
    org = data[2]
    update = data[3]

    videohref = None
    i = soup.find('div', {'class': " three-fourths"})
    for j in i.find_all('h3', {'style': "color:#4070B1;"}):
        if (j.get_text() == "Demo Video"):
            li = j.find_next_sibling("li")
            a = li.find('a')
            videohref = a['href']
            break

    darch = None
    i = soup.find('div', {'class': " three-fourths"})
    for j in i.find_all('h4', {'style': "font-style:italic;font-size:18px;margin:15px 0px;"}):
        if (j.get_text() == "7. Design Architecture"):
            li = j.find_next_sibling("div")
            darch = len(li)
            break

    git = []
    i = soup.find('div', {'class': " three-fourths"})
    for a in i.find_all('a'):
            aa = a['href']
            m = re.match(r"https://.*github.com\/.*$", aa)
            if (m):
                git.append(aa)

    git = list(set(git))

    mdgit = ""
    j = 1
    for i in git:
        mdgit = mdgit + " [[%d]](%s)" % (j, i,)
        j = j + 1

    if videohref:
        videohref = "[link](%s)" % (videohref,)
    else:
        videohref = ""

    t = teaminfo(team, category, leader, org, update, img, title, videohref, mdgit, darch)

    return t

team = "EM099"

teams = [ "EM112", "EM046", "EM080", "EM104", "EM051", "EM045", "EM057", "EM099", "EM016", "EM052", "EM075", "EM083", "EM071", "EM070", "EM077", "EM078", "EM113", "EM011", "EM039", "EM088", "EM116", "EM087", "EM055", "EM094", "EM076", "EM102", "EM043",  "EM097", "EM105", "EM084", "EM053" ]

def team_compare(x, y):
    lvx = len(x.videohref)
    lvy = len(y.videohref)
    if lvx > 0 and lvy == 0:
        return -1
    if lvy > 0 and lvx == 0:
        return 1

    lgx = len(x.mdgit)
    lgy = len(y.mdgit)
    if lgx > 0 and lgy == 0:
        return -1
    if lgy > 0 and lgx == 0:
        return 1

    if x.darch > 1 and y.darch == 1:
        return -1
    if y.darch > 1 and x.darch == 1:
        return 1

    return 0


infos = []

for team in teams:
    print team
    filename = "%s%s" % (PREFIX, team)
    #t = parse_one("http://" + filename)
    t = parse_one(filename)
    infos.append(t)

infos.sort(team_compare)

print("| n | team | title | update | image | video | github links | paper: design arch")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")


j = 1
for i in infos:
    size = 64
    fname = "img/" + i.team + ".jpg"
    sfname = "img/" + i.team + "_%d.jpg" % (size,)
    #os.system("curl -o %s %s" % (fname, i.img))
    #os.system("if [ ! -e %s ]; then wget -O %s %s; fi" % (fname, fname, i.img))
    #os.system("if [ ! -e %s ]; then convert %s -resize %dx%d %s; fi" % (sfname, fname, size, size, sfname))
    teamurl = "[%s](http://%s%s)" % (i.team, PREFIX, i.team)
    # (i.category + "; " + i.leader + "; " + i.org)
    imgurl = "![](%s?raw=true)" % (sfname,)
    md = "| %s | %s | %s | %s | %s | %s | %s |" % (teamurl, i.title, i.update, imgurl, i.videohref, i.mdgit, i.darch)
    print("| %d " % (j,) + md)
    j = j + 1

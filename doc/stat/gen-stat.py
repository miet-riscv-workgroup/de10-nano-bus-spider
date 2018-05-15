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

        title = title.replace("|", "&#124;")

        self.team = team
        self.title = title
        self.category = category
        self.leader = leader
        self.org = org
        self.update = update
        self.img = img

        self.videohref = videohref
        self.mdgit = mdgit
        self.darch = darch


def parse_one(team):

    url = "http://" + "%s%s" % (PREFIX, team)

    os.system("mkdir -p cache")

    filename = "cache/" + team + ".html"

    os.system("if [ ! -e %s ]; then wget -O %s %s 1>&2; fi" % (filename, filename, url))

    #resp = requests.get(url)
    #s = resp.text
    #soup = BeautifulSoup(s.encode('utf-8'), "lxml")

    #print(filename)
    with open(filename) as fp:
        s = fp.read()
        soup = BeautifulSoup(s.encode('utf-8'), "lxml")

    #print(soup.prettify())

    i = soup.find('div', {'class': " one-fourth"})
    if not i:
        i = soup.find('div', {'class': "one-fourth"})
    if not i:
        print "Warning: empty %s" % (team,)
        return
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
    if j:
        k = j.find('img')
        img = k['src']
    else:
        print("Warning: %s: no image" % (team,))
        img = None

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
            try:
                aa = a['href']
            except KeyError:
                continue
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

    if t is None:
        print("Warning: %s: teaminfo return None" % (team,))

    return t

import time
import datetime
def team_compare(x, y):
    assert (x)
    assert (y)

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

    xt = time.mktime(datetime.datetime.strptime(x.update, "%b %d, %Y").timetuple())
    yt = time.mktime(datetime.datetime.strptime(y.update, "%b %d, %Y").timetuple())
    if xt > yt:
        return -1
    if yt > xt:
        return 1

    return 0


def parse_region(teams):
    infos = []

    for team in teams:
        #print team
        t = parse_one(team)
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

        os.system("""
if [ ! -e %s ]; then
    wget -O %s %s
fi""" % (fname, fname, i.img))

        os.system("""
if [ ! -e %s ]; then
    convert %s -resize %dx%d! %s
fi""" % (sfname, fname, size, size, sfname))

        teamurl = "[%s](http://%s%s)" % (i.team, PREFIX, i.team)
        # (i.category + "; " + i.leader + "; " + i.org)
        imgurl = "![](%s?raw=true)" % (sfname,)
        md = "| %s | %s | %s | %s | %s | %s | %s |" % (teamurl, i.title, i.update, imgurl, i.videohref, i.mdgit, i.darch)
        print("| %d " % (j,) + md)
        j = j + 1

#teams = [ "EM112", "EM046", "EM080", "EM104", "EM051", "EM045", "EM057", "EM099", "EM016", "EM052", "EM075", "EM083", "EM071", "EM070", "EM077", "EM078", "EM113", "EM011", "EM039", "EM088", "EM116", "EM087", "EM055", "EM094", "EM076", "EM102", "EM043",  "EM097", "EM105", "EM084", "EM053" ]

#parse_region(teams)

#teams = [ "AS033", "AS031", "AS015", "AS032", "AS005", "AS023", "AS013", "AS018", "AS043", "AS039", "AS037", "AS028", "AS027", "AS021", "AS053", "AS054", "AS055", "AS058", "AS064", "AS050", "AS017", "AS025", "AS042", "AS066", "AS002" ]
#parse_region(teams)

#teams = [ "PR109", "PR022", "PR051", "PR026", "PR011", "PR061", "PR037", "PR087", "PR044", "PR066", "PR074", "PR015", "PR028", "PR095", "PR086", "PR062", "PR036", "PR138", "PR119", "PR075", "PR077", "PR081", "PR063", "PR137", "PR057", "PR076", "PR083", "PR089", "PR023", "PR129", "PR124", "PR050", "PR143", "PR144", "PR069", "PR029", "PR058", "PR148", "PR065", "PR121", "PR034", "PR082", "PR040", "PR107", "PR131", "PR060", "PR039", "PR123", "PR102", "PR072", "PR071" ]

#parse_region(teams)

#teams = [ "PR109", "PR022", "PR051", "PR026", "PR011", "PR061", "PR037", "PR087", "PR044", "PR066", "PR074", "PR015", "PR028", "PR095", "PR086", "PR062", "PR036", "PR138", "PR119", "PR075", "PR077", "PR081", "PR063", "PR137", "PR057", "PR076", "PR083", "PR089", "PR023", "PR129", "PR124", "PR050", "PR143", "PR144", "PR069", "PR029", "PR058", "PR148", "PR065", "PR121", "PR034", "PR082", "PR040", "PR107", "PR131", "PR060", "PR039", "PR123", "PR102", "PR072", "PR071" ]

teams = [ "AP074", "AP085", "AP068", "AP050", "AP062", "AP021", "AP042", "AP041", "AP071", "AP077", "AP028", "AP113", "AP027", "AP081", "AP116", "AP093", "AP121", "AP036", "AP030", "AP107", "AP034", "AP051", "AP026", "AP059", "AP112", "AP082", "AP075", "AP104", "AP089", "AP109", "AP038", "AP078", "AP095", "AP119", "AP066", "AP064" ]

parse_region(teams)

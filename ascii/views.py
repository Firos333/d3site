import datetime 
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json 
import os


def index(request):
    def add_item(item):
        context["tags"].append(item)

    with open('HTML_pages.txt') as f:
        link_list = f.readlines()
    link_list = [x.strip() for x in link_list] 
    print(link_list)
    size,length2,length3,match2,match3,Heading2, Heading3, headlink2, headlink3= ([] for i in range(9))

    for i in link_list:
        req = Request(i)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "lxml")
        links = []

        for link in soup.findAll('a'):
            links.append(link.get('href'))
        links = [link for link in links if link.startswith('#')]
        x=[link.replace('#','') for link in links]
        for link in x:
            if soup.find('h2', {'id': link}) != None:
                head = soup.find('h2', {'id': link}).text
                linked= i + '#' + str(link)
                headlink2.append(linked)
                Heading2.append(head)
                def match_class2(target):                                                        
                    def do_match(tag):                                                          
                        classes = tag.get('class', [])                                          
                        return all(c in classes for c in target)                                
                    return do_match                                                             
                match2 = soup.find_all(match_class2(["sect1"]))
            if soup.find('h3', {'id': link}) != None:
                head = soup.find('h3', {'id': link}).text
                linked= i + '#' + str(link)
                headlink3.append(linked)
                Heading3.append(head)
                def match_class3(target):                                                        
                    def do_match(tag):                                                          
                        classes = tag.get('class', [])                                          
                        return all(c in classes for c in target)                                
                    return do_match                                                             
                match3 = soup.find_all(match_class3(["sect2"]))
        for element in match3:
            length3.append(len(str(element)))
        for element in match2:
            length2.append(len(str(element)))

    Heading =Heading2 + Heading3
    Headlink = headlink2 + headlink3
    size = length2 + length3
    factor = 200
    cont_reduced= [(x / factor) for x in size]
    Font_size = [( x*1.5 if x<20 else x if 20<x<50 else x*0.65 if 50<x<200 else x*0.4) for x in cont_reduced]
    context={"tags" : [],}
  
    for lnk, txt, siz in zip(Headlink, Heading,Font_size):
        item = {}
        item["text"]= txt
        item["url"]= lnk
        item["size"]= int(siz)
        add_item(item)
        
    return render(request,'index.html',context)
def home(request):
    return render(request,'home.html')
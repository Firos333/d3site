import datetime 
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json 

def index(request):
    def add_item(item):
        context["tags"].append(item)
    req = Request("https://firos333.github.io/")
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    links = [link for link in links if link.startswith('#')]
    x=[link.replace('#','') for link in links]
    text=[]
    for link in x:
        results = soup.find(id= link)
        text.append(results.text)
    context={"tags" : [],}
    for lnk, txt in zip(links, text):
        item = {}
        item["text"]= txt
        item["url"]= 'https://firos333.github.io/'+lnk
        # item["country"]=..
        add_item(item)
    
    return render(request,'index.html',context)
def home(request):
    return render(request,'home.html')
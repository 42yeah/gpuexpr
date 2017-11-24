from django.shortcuts import render
from main.models import Passage, Pic
import random

# Create your views here.
def gen(con):
    entries = []
    if ((Passage.objects.all().__len__()) <= 5):
        entries = Passage.objects.all()
        con['entries'] = entries
        con['elen'] = entries.__len__()
        return con
    chose = []
    while (True):
        al = Passage.objects.all()
        r = random.randint(0, al.__len__() - 1)
        if r not in chose:
            print(r)
            chose.append(r)
            entries.append(al[r])
            if (chose.__len__() == 5):
                break
    con['entries'] = entries
    con['elen'] = 5
    return con

def index(request):
    con = {}
    return render(request, 'hello.html', gen(con))

def entry(request, e):
    ent = Passage.objects.filter(title=e)
    if (ent.__len__() <= 0):
        pass # no such entry 
    badges = ent[0].tags.split(' ')
    
    con = {
        'badges': badges,
        'p': ent[0],
    }
    return render(request, 'entry.html', gen(con))

def category(request, tag):
    grp = []
    l = 0
    for p in Passage.objects.all():
        tags = p.tags;
        t = tags.split(' ')
        for et in t:
            if (et == tag):
                l += 1
                d = {}
                d['title'] = p.title;
                d['author'] = p.author;
                if (p.body.__len__() > 100):
                    d['brief'] = p.body[:100] + '...'
                else:
                    d['brief'] = p.body
                grp.append(d)
        
    con = {
        'grp': grp,
        'category': tag,
        'l': l,
    }
    return render(request, 'category.html', gen(con))

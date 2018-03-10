from django.shortcuts import render
from main.models import Passage, Pic
import traceback
import os
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
    if (ent[0].body[:4] == 'PATH'):
        file = open(ent[0].body[4:], 'rb')
        try:
            ent[0].body = file.read().decode("gbk")
        except Exception as e:
            try:
                ent[0].body = file.read().decode("utf-8")
            except Exception as e:
                print('Cant decode')
                
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
                d['title'] = p.title
                d['author'] = p.author
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

def upload(request):
    try:
        f = request.FILES['f']
        file = open('media/' + f.name, 'wb')
        for chunk in f.chunks():
            file.write(chunk)
        file.close()
        file = open('media/' + f.name, 'r')
        os.system('soffice --headless --convert-to html --outdir "C:\\Users\\potio\\Documents\\gpuexpr\\media" "C:\\Users\\potio\\Documents\\gpuexpr\\media\\' + f.name + '"')
        spt = file.name.split('.')
        spt[len(spt) - 1] = 'html'
        fname = ''
        for s in spt:
            fname += s + '.'
        fname[len(fname) - 1] = ''
        print(fname)
        Passage.objects.create(
            title = request.POST['title'],
            author = request.POST['author'],
            body = 'PATH' + fname,
            tags = request.POST['tags']
        )
        con = {
            'succ': True
        }

    except Exception as e:
        print(e)
        con = {
            'succ': False
        }
    return render(request, 'upload.html', gen(con))

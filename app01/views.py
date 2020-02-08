from django.shortcuts import render,redirect
from app01.A import Axing
from app01.find import dic
import app01.RoadInfo as R
import time
now  = []
def mainwin(request):
    list = []
    ret = {}
    for key in dic:
        if dic[key][0] == '1':
            list.append([key,dic[key][2]])
    return render(request, "mainwin.html",{"list":list})
def mainwin2(request):
    list = []
    ret = {}
    for key in dic:
        if dic[key][0] == '2':
            list.append([key,dic[key][2]])
    return render(request, "mainwin2.html",{"list":list})
def mainwin3(request):
    list = []
    ret = {}
    for key in dic:
        if dic[key][0] == '3':
            list.append([key,dic[key][2]])
    return render(request, "mainwin3.html",{"list":list})
def mainwin4(request):
    list = []
    ret = {}
    for key in dic:
        if dic[key][0] == '4':
            list.append([key,dic[key][2]])
    return render(request, "mainwin4.html",{"list":list})
def mainwin5(request):
    list = []
    ret = {}
    for key in dic:
        if dic[key][0] == '5':
            list.append([key,dic[key][2]])
    return render(request, "mainwin5.html",{"list":list})
def path_choose(request):
    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        if (start in dic) and (end in dic):
            if Axing.main(start, end):
                time.sleep(0.5)
                return redirect("/path_choose_res/")
            else:
                return redirect("/path_choose_res2/")
        else:
            return redirect('/path_choose_err/')
    return render(request, 'path_choose.html')
def path_choose_err(request):
    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        if (start in dic) and (end in dic):
            if Axing.main(start, end):
                time.sleep(0.5)
                return redirect("/path_choose_res/")
            else:
                time.sleep(0.5)
                return redirect("/path_choose_res2/")
        else:
            redirect('/path_choose_err/')
    return render(request, 'path_choose_err.html')
def path_choose_res(request):
    return render(request, 'path_choose_res.html')
def path_choose_res2(request):
    return render(request, 'path_choose_res2.html')
def path_choose_busy(request):
    if request.method == "POST":
        if 'send' in request.POST:
            float = request.POST.get("float")
            road = request.POST.get("road")
            level = request.POST.get("level")
            now.append('层数：'+float+' '+'路段：'+road+' '+'程度：'+level)
            R.addInfo(float,road,level)
            print(now)
            print(R.Points)
        else:
            now.clear()
            R.Points.clear()
    ret = ['1','2','3','4','5']
    ret2 = ['a','b','c','d','e','f','g']
    ret3 = ['轻微拥堵','中度拥堵','严重拥堵']
    return render(request, 'path_choose_busy.html',{"list1":ret,"list2":ret2,"list3":ret3,"now":now})


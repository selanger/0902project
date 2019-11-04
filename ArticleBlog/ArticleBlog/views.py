from django.http import HttpResponse
from django.shortcuts import render


## 首页
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def listpic(request):
    return render(request,"listpic.html")

def newslistpic(request):
    return render(request,"newslistpic.html")
def base(request):
    return render(request,"base.html")









from django.shortcuts import render

# Create your views here.

from django.http.response import HttpResponse


def test(request):
    return HttpResponse("<h1>测试页面<h1>")


def index(request):
    return render(request, 'login/index.html')

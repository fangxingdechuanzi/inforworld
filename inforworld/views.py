from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
def start_view(request):
    return HttpResponseRedirect('/index/')

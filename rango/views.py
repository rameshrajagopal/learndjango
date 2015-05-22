from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'boldmessage' : 'I am bold font from this context'}
    return render(request, 'rango/index.html', context);


def about(request):
    context = {'boldmessage' : ' I am in about page bold font', 
               'message' : 'About page'}
    return render(request, 'rango/about.html', context)



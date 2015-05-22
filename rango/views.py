from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('''
            Rango says its hello world
            <a href='/rango/abou'>about</a>
            ''')


def about(request):
    return HttpResponse('''
            Rango says its about page
            <a href='/rango/'>Home</a>
            ''')


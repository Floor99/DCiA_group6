# views.py
from django.shortcuts import render
from django.http import JsonResponse
from . import plotly_app
def home(request):
    return render(request, 'ApolloSite/home.html')

def dashboard(request):
    return render(request, 'ApolloSite/dashboard.html')

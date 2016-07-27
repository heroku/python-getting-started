from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@login_required
def index(request):
    return render(request, 'recruit/home.html')

def new_search(request):
	return render(request, 'recruit/talent_search.html')

def campaign_detail(request):
	return render(request, 'recruit/campaign_detail.html')
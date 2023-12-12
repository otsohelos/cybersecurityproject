from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Account

@login_required
def homePageView(request):
	user = request.user
	accounts = Account.objects.filter(owner=user)
	return render(request, 'index.html', {'accounts': accounts})


# @login_required
# def homePageView(request):
# 	user = request.user
# 	accounts = Account.objects.filter(owner=user)
# 	return render(request, 'pages/index.html', {'accounts': accounts})
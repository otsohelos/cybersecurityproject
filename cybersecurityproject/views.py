from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Account, Message

@login_required
def homePageView(request):
	user = request.user
	accounts = Account.objects.filter(owner=user)
	users = User.objects.exclude(pk=request.user.id)
	return render(request, 'index.html', {'accounts': accounts, 'users': users})

@login_required
def addView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')
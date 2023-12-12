from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import sqlite3
import datetime

from .models import Account, Message

@login_required
def homePageView(request):
	user = request.user
	accounts = Account.objects.filter(owner=user)
	users = User.objects.exclude(pk=request.user.id)
	return render(request, 'index.html', {'accounts': accounts, 'users': users})

@login_required
def addView(request):
	target = User.objects.get(username=request.POST.get('to')).id
	source = request.user.id
	message = request.POST.get('content')
	conn = sqlite3.connect('db.sqlite3')
	cursor = conn.cursor()
	time = datetime.date.today()
	query =  "INSERT INTO cybersecurityproject_message (content, source_id, target_id, time) VALUES ('%s',%s, %s, %s)" % (message, source, target, time)
	cursor.execute(query)
	conn.commit()
	return redirect('/')

def latestView(request, user_id):
  messages = Message.objects.filter(target=user_id)
  return render(request, 'latest.html', {'messages': messages})

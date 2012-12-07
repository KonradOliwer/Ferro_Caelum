# coding=utf-8
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
import django.template.context as context

def login_user(request):
    state = "Logowanie"
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Logowanie pomyślne!"
            else:
                state = "Twoje konto nie jest aktywne."
        else:
            state = "Niepoprawny login i/lub hasło."


    return render_to_response('auth.html',
        {'state':state, 'username': username},
        context_instance=context.RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

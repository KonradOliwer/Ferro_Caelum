# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from registration.models import RegistrationForm
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from django.views.generic import TemplateView

def AccountRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            user.save()
            account = UserProfile(user=user)

            account.save()
            return HttpResponseRedirect('/registration/ok/')
        else:
            return render_to_response('register.html', {'form':form}, context_instance = RequestContext(request))
    else:
        ''' pusty formularz '''
        form = RegistrationForm()
        context ={'form': form}
        return render_to_response('register.html', context, context_instance = RequestContext(request))

class RegistrationOver(TemplateView):
    template_name = 'registration_k.html'
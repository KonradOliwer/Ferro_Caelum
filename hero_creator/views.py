# coding: utf-8
from django.http import HttpResponse
from django.template import Context, loader
from hero.models import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from user_profile.models import UserProfile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from functools import wraps
from django.contrib.auth.decorators import login_required

def no_hero_required(view):
    def wrap(request):
        profile = request.user.get_profile()
        if profile.hero == None:
             return view(request)
        else:
            return HttpResponseRedirect('/')
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap
 
@login_required
@no_hero_required
def start(request):
    template_name = loader.get_template('hero_creator/start.html')
    context = Context({
    })
    return HttpResponse(template_name.render(context))

@login_required
@no_hero_required
def blood_line(request):
    objects_list = BloodLine.objects.order_by('-name')
    try:
        picked_id = int(request.session.get('blood_line'))
    except TypeError:
        picked_id = None
    description = 'Wybór lini krwi:'
    no_objects_mesage = 'Nie istnieje ani jedna linii krwi w bazie danych.'
    back_link = '/hero_creator/start/'
    next_link = '/hero_creator/profession/'
    context = {
        'objects_list': objects_list,
        'picked_id': picked_id,
        'description': description,
        'no_objects_mesage': no_objects_mesage,
        'back_link': back_link,
        'next_link': next_link,
    }
    return render_to_response('hero_creator/choose_from_list.html', context,
        context_instance=RequestContext(request))

@login_required
@no_hero_required
def profession(request):
    if request.method == 'POST':
        request.session['blood_line'] = request.POST['object']
    objects_list = Profession.objects.order_by('-name')
    try:
        picked_id = int(request.session.get('profession'))
    except TypeError:
        picked_id = None
    description = 'Wybór profesji:'
    no_objects_mesage = 'Nie istnieje ani jedna profesja w bazie danych.'
    back_link = '/hero_creator/blood_line/'
    next_link = '/hero_creator/name/'
    context = {
        'objects_list': objects_list,
        'picked_id': picked_id,
        'description': description,
        'no_objects_mesage': no_objects_mesage,
        'back_link': back_link,
        'next_link': next_link,
    }
    return render_to_response('hero_creator/choose_from_list.html', context,
        context_instance=RequestContext(request))
    
@login_required
@no_hero_required    
def name(request):
    if request.method == 'POST':
        request.session['profession'] = request.POST['object']
    back_link = '/hero_creator/profession/'
    next_link = '/hero_creator/confirm/'
    description = 'Wybierz nazwę'
    context = Context({
        'description': description,
        'back_link': back_link,
        'next_link': next_link,
    })
    return render_to_response('hero_creator/choose_name.html', context,
        context_instance=RequestContext(request))

@login_required
@no_hero_required    
def confirm(request):
    if request.method == 'POST':
        request.session['name'] = request.POST['name']
    back_link = '/hero_creator/name/'
    next_link = '/hero_creator/end/'
    blood_line = BloodLine.objects.get(pk=request.session.get('blood_line'))
    profession = Profession.objects.get(pk=request.session.get('profession'))
    name = request.session.get('name')
    context = Context({
        'name': name,
        'profession': profession,
        'blood_line': blood_line,
        'back_link': back_link,
        'next_link': next_link,
    })
    return render_to_response('hero_creator/confirm.html', context,
        context_instance=RequestContext(request))

@login_required
@no_hero_required    
def end(request):
    if request.method == 'POST':
        profile = request.user.get_profile()
        hero = Hero.objects.create(name=request.session.get('name'),
            bloodline=BloodLine.objects.get(pk=request.session.get('blood_line')),
            profession=Profession.objects.get(pk=request.session.get('profession')))
        
        packages = Package.objects.filter(name="postac")
        if packages.exists():
            add_package(packages[0], hero)
                
        packages = Package.objects.filter(name="bohater")
        if packages.exists():
            add_package(packages[0], hero)
                
        profile.hero = hero        
        profile.save()
        del request.session['name']
        del request.session['blood_line']
        del request.session['profession']
    next_link = '/'
    context = Context({
        'next_link': next_link,
    })
    return render_to_response('hero_creator/end.html', context,
        context_instance=RequestContext(request))

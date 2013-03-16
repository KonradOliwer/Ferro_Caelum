# coding: utf-8

from django.http import HttpResponse
from django.template import Context, loader
from hero.models import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def start(request):
    template_name = loader.get_template('hero_creator/start.html')
    context = Context({
    })
    return HttpResponse(template_name.render(context))

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
    next_link = '/hero_creator/confirm/'
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
    
def confirm(request):
    if request.method == 'POST':
        request.session['profession'] = request.POST['object']
    back_link = '/hero_creator/profession/'
    next_link = '/hero_creator/end/'
    blood_line = BloodLine.objects.get(pk=request.session.get('blood_line'))
    profession = Profession.objects.get(pk=request.session.get('profession'))
    context = Context({
        'profession': profession,
        'blood_line': blood_line,
        'back_link': back_link,
        'next_link': next_link,
    })
    return render_to_response('hero_creator/confirm.html', context,
        context_instance=RequestContext(request))
    
def end(request):
    if request.method == 'POST':
        pass
    next_link = '/../../'
    context = Context({
        'next_link': next_link,
    })
    return render_to_response('hero_creator/end.html', context,
        context_instance=RequestContext(request))
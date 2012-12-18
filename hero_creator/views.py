# coding: utf-8

from django.http import HttpResponse
from django.template import Context, loader
from hero.models import BloodLine

def start(request):
    template = loader.get_template('hero_creator/start.html')
    context = Context({
    })
    return HttpResponse(template.render(context))

def blood_line(request):
    blood_line_list = BloodLine.objects.order_by('-name')
    template = loader.get_template('hero_creator/blood_line.html')
    context = Context({
        'blood_line_list': blood_line_list,
    })
    return HttpResponse(template.render(context))
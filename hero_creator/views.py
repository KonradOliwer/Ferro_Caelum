# coding: utf-8

from django.http import HttpResponse
from django.template import Context, loader
from hero.models import *

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
    if request.method == "POST":
        request.session['blood_line_id'] = POST['blood_line']
        return render_to_response('profession.html', context_instance=RequestContext(request))
#        return HttpResponseRedirect('/proffesion/')
    return HttpResponse(template.render(context))

def profession(request):
    profession_list = Profession.objects.order_by('-name')
    template = loader.get_template('hero_creator/profession.html')
    context = Context({
        'profession_list': profession_list,
    })
    return HttpResponse(template.render(context))
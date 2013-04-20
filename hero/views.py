from django.http import render_to_response
from django.template import RequestContext, loader

def stats_main(request):
    objects_list = BloodLine.objects.order_by('-name')
    hero = request.user.get_profile().hero
    context = {
        'hero': hero,
    }
    return render_to_response('hero/stats', context,
        context_instance=RequestContext(request))
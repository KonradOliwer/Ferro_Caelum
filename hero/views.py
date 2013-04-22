from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.db.models import Q

def stats_main(request):
    hero = request.user.get_profile().hero
    bars_base = hero.bars.filter(name__formula=None)
    bars_computable = hero.bars.filter(~Q(name__formula=None))
    stats_base = hero.stats.filter(name__formula=None)
    stats_computable = hero.stats.filter(~Q(name__formula=None))
    context = {
        'hero': hero,
        'bar_base': bars_base,
        'stats_base': stats_base,
        'bars_computable': bars_computable,
        'stats_computable': stats_computable,
    }
    return render_to_response('hero/stats.html', context,
        context_instance=RequestContext(request))
from django.views.generic import TemplateView
from django.template import RequestContext, loader
from django.http import HttpResponse
from user_profile.models import UserProfile
from hero.models import Hero
from django.contrib.auth.models import AnonymousUser

def homepage(request):
    main = loader.get_template('homepage.html')
    hero_creator = loader.get_template('hero_creator/start.html')
    user = request.user;
    context = RequestContext(request)
    if (request.user != AnonymousUser() and not request.user.get_profile().hero):
        return HttpResponse(hero_creator.render(context))
    else:
        return HttpResponse(main.render(context))

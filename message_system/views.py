# coding=utf-8
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from message_system.models import Message
from message_system.forms import ComposeForm

def inbox(request):
    """
    Skrzynka odbiorcza
    """
    message_list = Message.objects.inbox_for(request.user)
    return render_to_response('message_system/inbox.html', {
        'message_list': message_list,
        }, context_instance=RequestContext(request))

def outbox(request):
    """
    Skrzynka nadawcza
    """
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response('message_system/outbox.html', {
        'message_list': message_list,
        }, context_instance=RequestContext(request))

def view(request, message_id):
    """
    Wyświetlanie mejla
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if (message.author != user) and (message.receiver != user):
        raise Http404
    if message.read == False and message.receiver == user:
        message.read=True
        message.save()
    return render_to_response('message_system/view.html', {
        'message': message,
        }, context_instance=RequestContext(request))
view = login_required(view)

def compose(request, recipient=None, form_class=ComposeForm,
            template_name='message_system/compose.html'):
    """
    Komponowanie wiadomości elektronicznej
    """
    if request.method == "POST":

        form = form_class(request.POST)

        if form.is_valid():
            form.save(sender=request.user)
            messages.add_message(request, messages.SUCCESS, u"Wiadomość wysłana pomyślnie")
            return redirect('/')
    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(username__in=[r.strip() for r in recipient.split('+')])]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
        }, context_instance=RequestContext(request))
compose = login_required(compose)
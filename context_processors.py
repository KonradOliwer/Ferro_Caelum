from mail.models import inbox_count_for

def inbox(request):
    if request.user.is_authenticated():
        return {'inbox_count': inbox_count_for(request.user)}
    else:
        return {}


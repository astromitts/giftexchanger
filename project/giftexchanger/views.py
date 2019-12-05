from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect

from giftexchanger.models import UserProfile, GiftExchange, UserDetails
from giftexchanger.forms import EditUserDetailsForExchange


@login_required(login_url='login/')
def dashboard(request):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/app/dashboard.html')
    context = {
        'user': user,
        'exchanges': user.get_exchanges()
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_details(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/app/exchangedetails.html')
    exchange = GiftExchange.objects.get(pk=exc_id)
    user_details = UserDetails.objects.get(user=user, exchange=exchange)
    assignment = user.get_assignment(exchange)

    if assignment:
        assignment_details = UserDetails.objects.get(user=assignment, exchange=exchange)
    else:
        assignment_details = None
    is_exchange_admin = exchange in user.admin_of.all()
    context = {
        'user': user,
        'is_exchange_admin': is_exchange_admin,
        'exchange': exchange,
        'user_details': user_details,
        'assignment': assignment,
        'assignment_details': assignment_details
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_details_edit(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/app/exchangedetails_edit.html')
    exchange = GiftExchange.objects.get(pk=exc_id)
    user_details = UserDetails.objects.get(user=user, exchange=exchange)

    if request.POST:
        form = EditUserDetailsForExchange(request.POST)
        if form.is_valid:
            user_details.likes = request.POST['likes']
            user_details.dislikes = request.POST['dislikes']
            user_details.allergies = request.POST['allergies']
            user_details.save()
            return redirect('/exchangedetails/{}/'.format(exchange.pk))
    else:
        form = EditUserDetailsForExchange(instance=user_details)
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_admin(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/app/exchangeadmin.html')
    exchange = GiftExchange.objects.get(pk=exc_id)
    is_exchange_admin = exchange in user.admin_of.all()
    if not is_exchange_admin:
        return HttpResponseForbidden("Forbidden")
    context = {
        'exchange': exchange,
        'assignments': exchange.giftassignment_set.all()
    }
    return HttpResponse(template.render(context, request))

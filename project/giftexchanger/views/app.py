from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from giftexchanger.models import UserProfile, GiftExchange, UserDetails
from giftexchanger.forms.exchange_details import (
    EditUserDetailsForExchange,
    AdminEditExchangeInfo
)


@login_required(login_url='login/')
def user_dashboard(request):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/dashboard.html')
    context = {
        'user': user,
        'exchanges': user.get_exchanges()
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_details(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/exchange_details/details.html')
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
        'assignment_details': assignment_details,
        'breadcrumbs': [
            {'text': 'dashboard', 'url': reverse('user_dashboard')},
            {'text': exchange.title, 'url': None},
        ],
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_details_edit(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/exchange_details/edit.html')
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
    context = {
        'form': form, 
        'breadcrumbs': [
            {'text': 'dashboard', 'url': reverse('user_dashboard')},
            {'text': exchange.title, 'url': reverse('exchange_details', kwargs={'exc_id': exchange.pk})},
            {'text': 'Edit', 'url': None}
        ],
    }
    return HttpResponse(template.render(context, request))


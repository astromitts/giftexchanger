from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from giftexchanger.models import UserProfile, GiftExchange, UserDetails
from giftexchanger.forms.exchange_details import (
    AdminEditExchangeInfo
)


@login_required(login_url='login/')
def exchange_admin(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/exchange_admin/details.html')
    exchange = GiftExchange.objects.get(pk=exc_id)
    is_exchange_admin = exchange in user.admin_of.all()
    if not is_exchange_admin:
        return HttpResponseForbidden("Forbidden")
    context = {
        'exchange': exchange,
        'assignments': exchange.giftassignment_set.all(),
        'breadcrumbs': [
            {'text': 'Dashboard', 'url': reverse('user_dashboard')},
            {'text': exchange.title, 'url': reverse('exchange_details', kwargs={'exc_id': exchange.pk})},
            {'text': 'Admin', 'url': None}
        ],
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_admin_edit(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    exchange = GiftExchange.objects.get(pk=exc_id)
    is_exchange_admin = exchange in user.admin_of.all()
    if not is_exchange_admin:
        return HttpResponseForbidden("Forbidden")
    template = loader.get_template('giftexchanger/exchange_admin/edit_create.html')

    if request.POST:
        form = AdminEditExchangeInfo(request.POST)
        if form.is_valid:
            exchange.title = request.POST['title']
            exchange.description = request.POST['description']
            exchange.spending_max = request.POST['spending_max']
            exchange.schedule_day = request.POST['schedule_day']
            exchange.save()
            return redirect(reverse('exchange_admin', kwargs={'exc_id': exchange.pk}))
    else:
        form = AdminEditExchangeInfo(instance=exchange)
    context = {
        'form': form, 
        'back_url': reverse('exchange_details', kwargs={'exc_id': exchange.pk}),
        'breadcrumbs': [
            {'text': 'Dashboard', 'url': reverse('user_dashboard')},
            {'text': exchange.title, 'url': reverse('exchange_details', kwargs={'exc_id': exchange.pk})},
            {'text': 'Admin', 'url': reverse('exchange_admin', kwargs={'exc_id': exchange.pk})},
            {'text': 'Edit', 'url': None}
        ],
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_admin_create(request):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/exchange_admin/edit_create.html')

    if request.POST:
        form = AdminEditExchangeInfo(request.POST)
        if form.is_valid:
            exchange = GiftExchange()
            exchange.title = request.POST['title']
            exchange.description = request.POST['description']
            exchange.spending_max = request.POST['spending_max']
            exchange.schedule_day = request.POST['schedule_day']
            exchange.save()
            user.admin_of.add(exchange)
            user.save()
            new_user_details = UserDetails(user=user, exchange=exchange, likes="", dislikes="", allergies="")
            new_user_details.save()
            return redirect(reverse('exchange_admin', kwargs={'exc_id': exchange.pk}))
    else:
        new_exchange = GiftExchange()
        form = AdminEditExchangeInfo(instance=new_exchange)
    context = {
        'form': form, 
        'breadcrumbs': [
            {'text': 'Dashboard', 'url': reverse('user_dashboard')},
            {'text': 'Create Gift Exchange', 'url': None},
        ]
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def exchange_admin_add_users(request, exc_id):
    user = UserProfile.objects.get(pk=60)  # it me
    template = loader.get_template('giftexchanger/exchange_admin/add_users.html')
    exchange = GiftExchange.objects.get(pk=exc_id)
    is_exchange_admin = exchange in user.admin_of.all()
    if not is_exchange_admin:
        return HttpResponseForbidden("Forbidden")

    if request.POST:
        asdf
    else:
        available_users = UserProfile.objects.all()
        import pdb
        pdb.set_trace()
        context = {
            'exchange': exchange,
            'available_users': exchange.get_available_users(),
        }
        return HttpResponse(template.render(context, request))
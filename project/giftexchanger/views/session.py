from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from giftexchanger.forms.session import LoginUserForm


def login_handler(request):
    template = loader.get_template('giftexchanger/login.html')
    if request.user.is_authenticated:
        return redirect(reverse('user_dashboard'))
    if request.POST:
        data = request.POST.copy()
        form = LoginUserForm(data)
        if form.is_valid():
            try:
                user = User.objects.get(email=data['email'])
                if user.check_password(data['password']):
                    login(request, user)
                    return redirect(reverse('user_dashboard'))
                else:
                    context = {'login_form': form}
                    messages.error(request, 'Invalid password.')
                    return HttpResponse(template.render(context, request))
            except Exception:
                context = {'login_form': form}
                messages.error(request, 'Invalid email.')
                return HttpResponse(template.render(context, request))

    else:
        context = {'login_form': LoginUserForm}
        return HttpResponse(template.render(context, request))


def logout_handler(request):
    logout(request)
    return redirect(reverse('login_handler'))

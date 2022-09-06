from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import DOMAIN_LENGTH, DOMAIN,PATH, PATH_LENGTH, DOMAIN_PATH, Url
from .forms import ShortenUrlForm, RegistrationForm
from random import randint, choice
from time import sleep
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import URLValidator
# Create your views here.

urlvalidator = URLValidator(schemes=['http', 'https'])

def get_random_length():
    return randint(5,10)

def get_random_string(length):
    return ''.join(choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(length))

def get_random_short_url():
    return get_random_string(get_random_length())

def check_short_url(short_url,user):
    if Url.objects.filter(short_url=short_url, user=user).exists():
        return True
    return False

def check_long_url(long_url, user):
    if Url.objects.filter(long_url=long_url, user=user).exists():
        return True
    return False

@login_required(login_url='/login')
def index_handler(request):
    if request.method == "POST":
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            try :
                urlvalidator(form.cleaned_data['long_url'])
            except:
                return HttpResponse("Invalid URL, we only accept http or https urls.")
            if check_long_url(form.cleaned_data['long_url'], request.user):
                return HttpResponse("The long url is already in your list.")
            url = form.save(commit=False)
            url.short_url = get_random_short_url()
            url.user = request.user
            while check_short_url(url.short_url, url.user):
                url.short_url = get_random_short_url()
            url.save()
            return redirect(f'{PATH}{url.short_url}')
        else:
            return HttpResponse("The URL is either invalid or already exists.")
    else:
        urls = Url.objects.filter(user=request.user)
        form = ShortenUrlForm()
        return render(request, 'mainapp/index.html', {'form': form, 'urls': urls, 'domain': DOMAIN_PATH})


def link_handler(request,short_url):
   if request.method == "GET":
       url = Url.objects.get(short_url=short_url, user = request.user)
       url.redirect_count += 1
       url.save()
       return HttpResponseRedirect(url.long_url)

def register_handler(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("The username or email is already taken.")
    else:
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from Spinge.forms import ProfileForm, UserForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        auth = authenticate(username=username, password=password)
        if auth is not None:
            login(request, auth)
            return HttpResponseRedirect(reverse('spinge:index'))
        else:
            messages.add_message(request, messages.INFO, "Authentication Failed!")
            return HttpResponseRedirect(reverse('home'))

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('spinge:index'))
    else:
        return render(request, 'login.html')


def home_view(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.profile.is_student = profile_form.cleaned_data.get('student')
            user.profile.is_professor = profile_form.cleaned_data.get('professor')
            user.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.add_message(request, messages.INFO, "Signup Successful")
            return redirect('home')

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})



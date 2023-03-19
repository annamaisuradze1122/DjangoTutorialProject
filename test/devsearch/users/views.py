from urllib import request
from django.urls import is_valid_path
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Profile, Skill
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db.models import Q

# Create your views here.


def profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print(search_query)

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        )
    context={'profiles': profiles, 'search_query':search_query}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    context = {'profile':profile, 'topSkills':topSkills,'otherSkills':otherSkills }
    return render(request,'users/user_profile.html', context)


def user_login(request):
    page = 'login'
    #0 Check if the user is authenthicated
    if request.user.is_authenticated:
        return redirect('profiles')

    #1 Get the entered value
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']   

    #2 Check if user with this username exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

    #3 authenthicate and log in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid data')
    context = {'page':page}
    return render(request, 'users/login_register.html', context)


def user_logout(request):
    logout(request)
    messages.success(request,'User was logged out')
    return redirect('login')


def user_register(request):
    page ='register'
    form = CustomUserCreationForm()

    if request.method == "POST":
       form =  CustomUserCreationForm(request.POST)
       if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"Registered")
            login(request, user)
            return redirect('login')
       else:   
        messages.error(request,"Registration Error")

    context ={ 'page':page,'form':form }
    return render(request, 'users/login_register.html', context)

@login_required
def get_user_account(request,):
    user = request.user
    profile = Profile.objects.get(username=user.username)
    print(profile.username, profile.name, profile.email),
    context = {'profile':profile}
    return render(request, 'users/account.html', context)


@login_required
def edit_user_account(request):
    user = request.user
    profile = Profile.objects.get(username=user.username)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles')
    context = {'form':form}
    return render(request, 'users/account_form.html', context)


